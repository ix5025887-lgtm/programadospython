"""
Classe base para todos os serviços do sistema.
Abstração da camada de acesso a dados.
"""
from typing import Any, Dict


class BaseService:
    """Serviço base com métodos comuns"""
    
    def __init__(self) -> None:
        """Inicializa o serviço"""
        pass
    
    def _validar_dados(self, **kwargs: Any) -> bool:
        """Validação genérica de dados
        
        Args:
            **kwargs: Pares chave-valor a validar
            
        Returns:
            bool: True se todos os dados são válidos
            
        Raises:
            ValueError: Se algum valor for vazio ou None
        """
        for chave, valor in kwargs.items():
            if valor is None or valor == "":
                raise ValueError(f"{chave} não pode ser vazio")
        return True
