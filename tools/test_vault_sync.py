#!/usr/bin/env python3
"""Check remote updates and Windows copies with disposable repositories."""
import os
import json
import signal
from pathlib import Path
import subprocess
import tempfile
import time

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


def main():
    with tempfile.TemporaryDirectory(prefix='mephi-sync-') as directory:
        root = Path(directory)
        remote, source, writer, dest = [root / name for name in ('remote.git', 'source', 'writer', 'windows')]
        env = dict(os.environ, GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null',
                   MEPHI_SYNC_SOURCE=str(source), MEPHI_SYNC_DEST=str(dest),
                   MEPHI_SYNC_STATE=str(root / 'state'), MEPHI_SYNC_ORIGIN=str(remote))

        def run(*args, ok=True):
            result = subprocess.run(args, env=env, text=True, capture_output=True, timeout=40)
            if ok and result.returncode:
                raise AssertionError(result.stderr + result.stdout)
            return result

        def git(repo, *args):
            return run('git', '-C', str(repo), *args).stdout.strip()

        def commit(repo, message):
            git(repo, 'add', '.')
            git(repo, 'commit', '-qm', message)

        def script(name, ok=True):
            return run('bash', str(SCRIPTS / name), ok=ok)

        run('git', 'init', '--bare', '--initial-branch=main', str(remote))
        run('git', 'clone', str(remote), str(writer))
        git(writer, 'config', 'user.name', 'Sync test')
        git(writer, 'config', 'user.email', 'test@example.invalid')
        (writer / '00-standards').mkdir()
        (writer / 'CLAUDE.md').write_text('Test instructions.\n')
        (writer / '00-standards/documentation-standard.md').write_text('Test standard.\n')
        (writer / 'note.md').write_text('First version.\n')
        commit(writer, 'Initial content')
        git(writer, 'push', 'origin', 'main')
        run('git', 'clone', str(remote), str(source))
        git(source, 'config', 'user.name', 'Sync test')
        git(source, 'config', 'user.email', 'test@example.invalid')
        script('sync-mephi-vault-to-windows.sh')
        assert (dest / 'note.md').read_text() == 'First version.\n'
        assert not (dest / '.git').exists()

        (writer / 'note.md').write_text('Remote version.\n')
        commit(writer, 'Update content')
        git(writer, 'push', 'origin', 'main')
        script('refresh-mephi-vault.sh')
        assert git(source, 'rev-parse', 'HEAD') == git(writer, 'rev-parse', 'HEAD')
        script('sync-mephi-vault-to-windows.sh')
        assert (dest / 'note.md').read_text() == 'Remote version.\n'

        (source / 'note.md').write_text('Local draft.\n')
        before = git(source, 'rev-parse', 'HEAD')
        (writer / 'remote.md').write_text('New remote page.\n')
        commit(writer, 'Add remote page')
        git(writer, 'push', 'origin', 'main')
        script('refresh-mephi-vault.sh')
        assert git(source, 'rev-parse', 'HEAD') == before
        assert (source / 'note.md').read_text() == 'Local draft.\n'
        (source / '.env').write_text('SYNTHETIC_SECRET=excluded\n')
        script('sync-mephi-vault-to-windows.sh')
        assert (dest / 'note.md').read_text() == 'Local draft.\n'
        assert not (dest / '.env').exists()
        (source / '.env').unlink()
        (dest / '.obsidian').mkdir()
        (dest / '.obsidian/appearance.json').write_text('{}')
        script('sync-mephi-vault-to-windows.sh')
        assert (dest / '.obsidian/appearance.json').read_text() == '{}'

        # Shared colors update without replacing newer personal graph settings.
        (source / '.obsidian').mkdir()
        graph_source = source / '.obsidian/graph.json'
        graph_dest = dest / '.obsidian/graph.json'
        colors = [{'query': 'path:"development/"', 'color': {'a': 1, 'rgb': 5088255}}]
        graph_source.write_text(json.dumps({'colorGroups': colors, 'scale': 1}))
        personal_graph = {'colorGroups': [], 'scale': 3, 'showOrphans': False}
        graph_dest.write_text(json.dumps(personal_graph))
        os.utime(graph_dest, (time.time() + 20, time.time() + 20))
        run('bash', str(SCRIPTS / 'sync-mephi-vault-to-windows.sh'), '--dry-run')
        assert json.loads(graph_dest.read_text()) == personal_graph
        script('sync-mephi-vault-to-windows.sh')
        assert json.loads(graph_dest.read_text()) == dict(personal_graph, colorGroups=colors)
        assert (dest / '.obsidian/appearance.json').read_text() == '{}'
        graph_backups = list((root / 'state/backups').rglob('graph.json'))
        assert any(json.loads(p.read_text()) == personal_graph for p in graph_backups)
        unchanged_graph = graph_dest.read_bytes()
        script('sync-mephi-vault-to-windows.sh')
        assert graph_dest.read_bytes() == unchanged_graph
        assert len(list((root / 'state/backups').rglob('graph.json'))) == len(graph_backups)
        graph_source.write_text('{invalid')
        assert script('sync-mephi-vault-to-windows.sh', ok=False).returncode != 0
        assert graph_dest.read_bytes() == unchanged_graph
        graph_source.write_text(json.dumps({'colorGroups': colors}))
        (source / '.obsidian').rename(source / 'saved-graph-settings')
        script('sync-mephi-vault-to-windows.sh')
        assert graph_dest.read_bytes() == unchanged_graph
        (source / 'saved-graph-settings').rename(source / '.obsidian')

        (dest / 'note.md').write_text('Newer Windows edit.\n')
        os.utime(dest / 'note.md', (time.time() + 20, time.time() + 20))
        script('sync-mephi-vault-to-windows.sh')
        assert (dest / 'note.md').read_text() == 'Newer Windows edit.\n'
        (source / 'CLAUDE.md').write_text('Changed instructions.\n')
        script('sync-mephi-vault-to-windows.sh')
        backups = root / 'state/backups'
        assert any(p.read_text() == 'Test instructions.\n' for p in backups.rglob('CLAUDE.md'))
        (source / 'note.md').unlink()
        script('sync-mephi-vault-to-windows.sh')
        assert not (dest / 'note.md').exists()
        assert any(p.read_text() == 'Newer Windows edit.\n' for p in backups.rglob('note.md'))

        commit(source, 'Local changes')
        local_head = git(source, 'rev-parse', 'HEAD')
        script('refresh-mephi-vault.sh')
        assert git(source, 'rev-parse', 'HEAD') == local_head
        git(source, 'switch', '-c', 'test-other')
        (source / 'wrong-branch.md').write_text('Do not mirror.\n')
        script('sync-mephi-vault-to-windows.sh')
        assert not (dest / 'wrong-branch.md').exists()
        git(source, 'switch', 'main')
        git(source, 'remote', 'set-url', 'origin', str(root / 'missing.git'))
        assert script('refresh-mephi-vault.sh', ok=False).returncode != 0
        env['MEPHI_SYNC_ORIGIN'] = str(root / 'missing.git')
        assert script('refresh-mephi-vault.sh', ok=False).returncode != 0
        (source / 'offline.md').write_text('Local copy needs no network.\n')
        script('sync-mephi-vault-to-windows.sh')
        assert (dest / 'offline.md').exists()
        daemon = subprocess.Popen(['bash', str(SCRIPTS / 'start-mephi-vault-sync.sh'), '--run'],
                                  env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  start_new_session=True)
        try:
            (source / 'watched.md').write_text('Automatic local update.\n')
            colors[0]['color']['rgb'] = 11766015
            graph_source.write_text(json.dumps({'colorGroups': colors}))
            deadline = time.monotonic() + 10
            while (not (dest / 'watched.md').exists() or
                   json.loads(graph_dest.read_text())['colorGroups'] != colors) and time.monotonic() < deadline:
                time.sleep(0.2)
            assert (dest / 'watched.md').read_text() == 'Automatic local update.\n'
            assert json.loads(graph_dest.read_text()) == dict(personal_graph, colorGroups=colors)
            assert daemon.poll() is None
        finally:
            daemon.send_signal(signal.SIGTERM)
            try:
                daemon.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(daemon.pid, signal.SIGKILL)
                daemon.wait()
                raise
        assert not (root / 'state/daemon.pid').exists()
        print('PASS: graph colors and personal settings, dry run, invalid configuration, daemon copy and shutdown, remote fast-forward, local drafts, exclusions, Windows edits, backups, deletion, divergence, branch guard and offline copy.')


if __name__ == '__main__':
    main()
