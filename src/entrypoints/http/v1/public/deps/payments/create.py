from src.application.usecases.payments.create import Usecase


def dependency() -> Usecase:
    return Usecase()
