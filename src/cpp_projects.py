import os
import requests
import traceback
from requests.exceptions import RequestException
from git import Repo
    

class New_CPP_Project:
    def __init__(self, project_base_dir:str) -> None:
        self.project_base_dir = project_base_dir
        self.user_path = os.path.expanduser('~/Programming/cpp_dev/')
        self.user_license_pref = "GPL"
        os.chdir(f'{self.user_path}/{self.project_base_dir}')
        """
        Add os checking and dynamic file paths before backup_file_locs is fully functional.
        Also need to move this file to its own project. 
        """
        self.backup_file_locs = {'gitignore': 'add file locs',
                                 'GPL_license' : 'add file locs',
                                 'readme' : 'add file locs',}
        
        self.sub_dirs = ['app',
                         'build',
                         'cmake',
                         'docs',
                         'include',
                         'src',
                         'tests']
        
        self.base_dir_files = {'README.md':'https://gist.githubusercontent.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc/raw/d59043abbb123089ad6602aba571121b71d91d7f/README-Template.md',
                               'LICENSE.md': ['https://www.gnu.org/licenses/gpl-3.0.txt', 'https://gist.githubusercontent.com/adamveld12/b64e74d14d7d9043b85c/raw/2d4cf3afe445b79c3b496ce67e9d2ab3365232dd/LICENSE.txt'],
                               '.gitignore': 'https://raw.githubusercontent.com/github/gitignore/main/C%2B%2B.gitignore'}


    def _get_base_dir_docs(self, file_name:str) -> str|None:
        try:
            response = requests.get(self.base_dir_files[file_name])
            return response.content.decode()
        except RequestException as req_error:
            print(f'{req_error} \n\n {traceback.format_exc()}')
            return None


    def _write_a_file(self, file_name:str, file_content:str|None) -> None:
        if file_content is not None:
            try:
                with open(f'{file_name}', 'x') as a_file:
                    a_file.write(file_content)
            except FileExistsError as fl_error:
                print(f'{fl_error} \n\n {traceback.format_exc()}')
        else:
            print(f"Couldn't create {file_name}.")


    def build_dir_struct(self) -> None:
        for dir in self.sub_dirs:
            try:
                os.mkdir(dir)
                print(f'{dir} created')
            except FileExistsError as e:
                print(f'{e}')

# https://gitpython.readthedocs.io/en/stable/quickstart.html?highlight=git%20add#add-file-to-staging-area
    def setup_git(self) -> None:
        new_repo = Repo.init(os.getcwd())
        for file_name in self.base_dir_files.keys():
            match (file_name):
                case ('README.md'):
                    readme = self._get_base_dir_docs(file_name)
                    self._write_a_file(file_name, readme)
                case ('LICENSE.md'):
                    gpl_license = self._get_base_dir_docs(file_name[0])
                    self._write_a_file(file_name[0], gpl_license)
                case ('gitignore'):
                    gitignore = self._get_base_dir_docs(file_name)
                    self._write_a_file(file_name, gitignore)
                    
        new_repo.index.add(list(self.base_dir_files.keys()))
