from flask import Flask
import os
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, Model

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


db.create_all()

names = {
    "tim": {"age": 19, "gender": "male"},
    "bill": {"age": 65, "gender": "male"}
}

resource_fields = {
    "id": fields.Integer,
    "views": fields.Integer,
    "likes": fields.Integer,
    "name": fields.String,
}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the Video", required=True)
video_put_args.add_argument("views", type=int, help="Views of the Video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the Video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the Video")
video_update_args.add_argument("views", type=int, help="Views of the Video")
video_update_args.add_argument("likes", type=int, help="Likes of the Video")


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video is missing...")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video is taken...")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video is missing...")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.name = args['views']
        if args['likes']:
            result.name = args['likes']

        db.session.commit()

        return result

    @marshal_with(resource_fields)
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video is missing...")
        db.session.delete(result)
        db.session.commit()
        return '', 204


class Videos(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = VideoModel.query.all()
        return result


api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(Videos, "/video")

if __name__ == '__main__':
    app.run(debug=True)
