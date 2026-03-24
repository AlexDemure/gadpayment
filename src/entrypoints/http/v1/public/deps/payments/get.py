from src.application.usecases.payments.get import Usecase


def dependency() -> Usecase:
    return Usecase()
