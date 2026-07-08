from validation.validation_result import ValidationResult


class EnvironmentValidator:

    def __init__(
        self,
        driver,
        excel_path=None
    ):
        self.driver = driver
        self.excel_path = excel_path

    def validate(self):

        errors = []

        # We'll add checks here

        return ValidationResult(
            success=len(errors) == 0,
            errors=errors
        )