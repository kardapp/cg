from pydantic import BaseModel


class ValidationError(BaseModel):
    field: str
    message: str


class UserNotAssociatedWithCustomerError(ValidationError):
    field: str = "customer"
    message: str = "User does not belong to customer"


class TicketNumberRequiredError(ValidationError):
    field: str = "ticket_number"
    message: str = "Ticket number is required"


class CustomerCannotSkipReceptionControlError(ValidationError):
    field: str = "skip_reception_control"
    message: str = "Customer cannot skip reception control"


class CustomerDoesNotExistError(ValidationError):
    field: str = "customer"
    message: str = "Customer does not exist"


class OrderNameRequiredError(ValidationError):
    field: str = "name"
    message: str = "Order name is required"

class OccupiedWellError(ValidationError):
    field: str = "well"
    message: str = "Well is occupied"
