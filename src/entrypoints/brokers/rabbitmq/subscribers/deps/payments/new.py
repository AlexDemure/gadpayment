from src.application.usecases.payments.new import Usecase


def dependency() -> Usecase:
    return Usecase()
