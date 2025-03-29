import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Optional


class EnvManager:
    def __init__(self):
        self._possible_keys = ['DEFAULT_EXPORT_BASE_PATH', 'DEFAULT_IMPORT_FILE_NAME', 'DEFAULT_EXPORT_FILE_NAME']
        self._default_path = './Files'
        self._init_envs()

    def get_env(self, env_name: str) -> str:
        """
        Obtém uma variável de ambiente com fallback opcional

        Args:
            env_name: Nome da variável de ambiente
        Returns:
            Valor da variável de ambiente ou o padrão
        Raises:
            ValueError: Se a variável não for suportada ou não existir
        """
        if env_name not in self._possible_keys:
            self._print_supported_keys()
            raise ValueError(f"A variável [{env_name}] não é suportada")
        return os.getenv(env_name).replace('\\', '/')

    def _init_envs(self):
        """Inicializa o arquivo .env com valores padrão se não existir"""
        env_path = Path(__file__).parent.parent / '.env'

        if not env_path.exists():
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(f"DEFAULT_EXPORT_BASE_PATH='{self._default_path}'\n")
                f.write("DEFAULT_IMPORT_FILE_NAME='archidekt'\n")
                f.write("DEFAULT_EXPORT_FILE_NAME='py_magic'\n")

            os.makedirs(self._default_path, exist_ok=True)

        load_dotenv(env_path)

    def _print_supported_keys(self):
        """Exibe as variáveis de ambiente suportadas"""
        print("Variáveis de ambiente suportadas:")
        for key in self._possible_keys:
            print(f"  - {key}")

# env = EnvManager()
#
# # 1. Uso básico
# base_path = env.get_env('BASE_PATH')
#
# print('BASE_PATH: ' + base_path + '\n')
#
# # 2. Com valor padrão alternativo
# output_name = env.get_env('NON_COMMANDER_OUTPUT_NAME')
#
# # 3. Tratamento de erros
# try:
#     value = env.get_env('VAR_INVALIDA')
# except ValueError as e:
#     print(e)
