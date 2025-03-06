import logging

from flask_restful import Resource, reqparse  # type: ignore
from werkzeug.exceptions import InternalServerError, NotFound

import services
from controllers.service_api import api
from controllers.service_api.wraps import FetchUserArg, WhereisUserArg, validate_app_token
from controllers.web.error import AppUnavailableError

from models.model import App, EndUser
from services.annotation_service import AppAnnotationService


class AnnotationApi(Resource):
    @validate_app_token(fetch_user_arg=FetchUserArg(fetch_from=WhereisUserArg.JSON, required=True))
    def post(self, app_model: App, end_user: EndUser):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, location="json")
        parser.add_argument("question", type=str, location="json")
        parser.add_argument("time", type=str, location="json")

        args = parser.parse_args()

        try:
            response = AppAnnotationService.get_annotation_list_all_by_app_id(
                user=end_user,
                app_id=str(app_model.id),
                question=args["question"],
                time=args["time"],
                annotation_id=args["id"]
            )
            return response, 200
        except services.errors.app_model_config.AppModelConfigBrokenError:
            logging.exception("App model config broken.")
            raise AppUnavailableError()
        except ValueError as e:
            raise e
        except Exception as e:
            logging.error(e)
            logging.exception("internal server error.")
            raise InternalServerError()


api.add_resource(AnnotationApi, "/message-annotations")