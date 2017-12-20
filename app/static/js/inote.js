
    var NoteLoader = function(){
        prototype.getData = function(){};
        prototype.setData = function(){};
        prototype.loader = function(){};

    };

    /**
    * Note Class
    */

    var NoteClass = function(NoteCateId,EditorType,NoteId,NoteTitle,NoteContent){
        var EditorTypes =   [
                                {
                                    "name"      : Null,
                                    "loader"    : function(){},
                                },
                            ];

        var id = Null;

        var note_category_id = Null;
        var title = Null;
        var content = Null;
        var create_datetime = Null;
        var last_modify_datetime = Null;

        var setEditType = function(EditorType)
        {
            if(!edit_type){
                edit_type = EditorTypes["ckeditor"];
            }
            if(typeof EditorType == string)
            {
                edit_type = EditorTypes[EditorType];
            }else{
                edit_type = EditorType;
            }
            if(edit_type == EditorTypes.Null)
            {
                throw "edit type is null";
            }
        };
        var registEditType = function(EditorType,callback)
        {
            if(!(EditorType && callback))
            {
                EditorTypes[EditorType] = callback;
            }
            else
                throw "regist edit type error";
        };
        var setEditType = function(EditorType)
        {

        }

    };
