import logging

from flask_restful import Resource, reqparse, marshal  # type: ignore
from werkzeug.exceptions import InternalServerError
from controllers.service_api import api
from controllers.service_api.wraps import FetchUserArg, WhereisUserArg, validate_app_token
from fields.annotation_fields import annotation_fields
from models.model import App, EndUser
from services.annotation_service import AppAnnotationService


class AnnotationApi(Resource):
    @validate_app_token(fetch_user_arg=FetchUserArg(fetch_from=WhereisUserArg.QUERY))
    def get(self, app_model: App, end_user: EndUser):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, location="args")
        parser.add_argument("question", type=str, location="args")
        parser.add_argument("time", type=str, location="args")

        args = parser.parse_args()

        try:
            annotation_list = AppAnnotationService.get_annotation_list_all_by_app_id(
                tenant_id=end_user.tenant_id,
                app_id=str(app_model.id),
                question=args["question"],
                time=args["time"],
                annotation_id=args["id"]
            )
            response = {"result": "success", "data": marshal(annotation_list, annotation_fields)}
            return response, 200
        except Exception as e:
            logging.error(e)
            logging.exception("internal server error.")
            raise InternalServerError()


api.add_resource(AnnotationApi, "/message-annotations")