import os
import pytest
from guiem import ShellEmulatorGUI 

@pytest.fixture
def setup_vfs():
    # Укажите путь к уже существующему tar-файлу
    tar_path = "D:\projects\cfg\vfs1.tar"  # Замените на актуальный путь к вашему tar-файлу
    yield tar_path

def test_ls(setup_vfs):
    gui = ShellEmulatorGUI(None)
    gui.current_dir = gui.extract_vfs(setup_vfs)
    
    output = gui.ls(gui.current_dir)
    
    assert "file1.txt" in output
    assert "file2.txt" in output

def test_cd_valid(setup_vfs):
    gui = ShellEmulatorGUI(None)
    gui.current_dir = gui.extract_vfs(setup_vfs)
    
    new_dir = "some_subdirectory"
    os.makedirs(os.path.join(gui.current_dir, new_dir), exist_ok=True)
    
    new_path = gui.cd(gui.current_dir, new_dir)
    
    assert new_path == os.path.join(gui.current_dir, new_dir)

def test_cd_invalid(setup_vfs):
    gui = ShellEmulatorGUI(None)
    gui.current_dir = gui.extract_vfs(setup_vfs)
    
    with pytest.raises(FileNotFoundError):
        gui.cd(gui.current_dir, "non_existing_directory")

def test_whoami():
    gui = ShellEmulatorGUI(None)
    user = gui.whoami()
    
    assert user == os.getlogin()

def test_mv(setup_vfs):
    gui = ShellEmulatorGUI(None)
    gui.current_dir = gui.extract_vfs(setup_vfs)
    
    source = "file1.txt"
    destination = "moved_file1.txt"
    
    gui.mv(os.path.join(gui.current_dir, source), os.path.join(gui.current_dir, destination))
    
    assert os.path.exists(os.path.join(gui.current_dir, destination))
    assert not os.path.exists(os.path.join(gui.current_dir, source))

def test_tree(setup_vfs):
    gui = ShellEmulatorGUI(None)
    gui.current_dir = gui.extract_vfs(setup_vfs)
    
    output = gui.tree(gui.current_dir)
    
    assert "file1.txt" in output
    assert "file2.txt" in output

if __name__ == "__main__":
    pytest.main()
