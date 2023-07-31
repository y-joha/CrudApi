from flask import Flask, request
from flask_restful import Api , Resource, reqparse, abort, fields, marshal_with 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"
    


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name" , type=str , help="Name of video is required",required=True)
video_put_args.add_argument("views" , type=int , help="Number of Views",required=True)
video_put_args.add_argument("likes" , type=int , help="number of likes",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name" , type=str , help="Name of video is required")
video_update_args.add_argument("views" , type=int , help="Number of Views")
video_update_args.add_argument("likes" , type=int , help="number of likes")

resource_fields = {
    'id': fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
}

        
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found with this ID")
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video_id already exists")
        video = VideoModel(id=video_id,name = args['name'],views = args['views'],likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found with this ID")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()
        return result
            
    
    def delete(self, video_id):
        del videos[video_id]
        return '', 204
    
api.add_resource(Video, "/video/<int:video_id>")

#only for testing purposes
if __name__ == '__main__':
    app.run(debug=True)