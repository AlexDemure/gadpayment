from src.common.http.collections import HTTPError


class PaymentNotFound(HTTPError): ...


class PaymentAlreadyExists(HTTPError): ...
