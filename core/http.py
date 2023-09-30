from rest_framework.response import Response as DrfRespnose
from rest_framework.exceptions import APIException
from core.enum import choice


class APIError(APIException):
    status_code = 406
    default_detail = choice.GENERAL_API_ERROR_MSG
    default_code = choice.RESPONSE_CODE_FAILED

    def __init__(self, detail=None, code=None, status_code=None):
        if detail:
            self.default_detail = detail
        if code:
            self.default_code = code

        if status_code:
            self.status_code = status_code

        self.detail = self.get_full_details()

    def get_full_details(self):
        return {
            "meta": {
                "success": False,
                "code": self.default_code,
            },
            "result": {"detail": self.default_detail},
        }


class Response(DrfRespnose):
    def __init__(
        self,
        data=None,
        code=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        result = {
            "meta": {
                "success": True,
                "code": (code if code else choice.RESPONSE_CODE_SUCCESS),
            },
            "result": data,
        }

        super().__init__(
            data=result,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
