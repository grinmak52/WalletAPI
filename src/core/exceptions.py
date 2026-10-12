class WalletNotFoundError(Exception):
    """Кошелёк не найден."""


class InsufficientFundsError(Exception):
    """Недостаточно средств на кошельке."""
