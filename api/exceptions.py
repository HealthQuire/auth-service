from fastapi import HTTPException, status


class TwoOrNoneSeed(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail="You need to specify mnemonic or seed")


class InvalidMnemonic(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail="Invalid mnemonic")


class InvalidSeed(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail="Invalid seed")


class AddressOrId(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail="You need to specify address or telegram id")


class WalletNotExist(HTTPException):
    def __init__(self, telegram_id) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail=f"Wallet with telegram id {telegram_id} is not exist")


class NotEnoughTokens(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail="You don't have enough tokens")
