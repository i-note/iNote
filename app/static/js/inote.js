/*
    var Singleton = function(){};
    Singleton.prototype = {
         getInstance:function(){
            arguments.callee.instance = arguments.callee.instance || {};
            return arguments.callee.instance;
        }
    };
    var singleton = new Singleton();
*/


    var EditorTypeInterface = function(name){
        this.editor_name = name;
    };
    EditorTypeInterface.prototype = {
        editor_name : "",
        construct : function(){
            throw "inote editor exception: function need override.";
        },
        destruct : function(){
            throw "inote editor exception: function need override.";
        },
        getData : function(){
            throw "inote editor exception: function need override.";
        },
        setData : function(data){
            throw "inote editor exception: function need override.";
        },
    };

    var NoteSingleton= function(){};
    NoteSingleton.prototype = {
         getInstances:function(){
            NoteSingleton.instance = NoteSingleton.instance || {};
            return NoteSingleton.instance;
         },
         getInstance:function(name){
            NoteSingleton.instance = NoteSingleton.instance || {};
            return NoteSingleton.instance[name];
         },
         addInstance:function(instance){
            NoteSingleton.instance = NoteSingleton.instance || {};
            if(instance instanceof EditorTypeInterface)
            {
                if (instance.editor_name == undefined)
                    throw "inote editor exception: editor_name cannot undefined.";
                NoteSingleton.instance[instance.editor_name]=instance;
            }
         }
    };

    var note = new NoteSingleton;

    var Inote_CKEditor = function(name){
        if(!name)
            this.editor_name =  "ckeditor";
        else
            this.editor_name = name;
        prototype = new EditorTypeInterface(this.editor_name);

        this.construct=function(){
            console.log("test");
        }
    };
    note.addInstance(new Inote_CKEditor);

    /**
    * Note Class
    */

     function Note(NoteCateId,EditorType,NoteId,NoteTitle,NoteContent){
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

        this.setEditType = function(EditorType)
        {
            if(edit_type == EditorTypes.Null)
            {
                throw "edit type is null";
            }
        };
        this.registEditorTypeInterface = function(interface)
        {
            if(interface instanceof EditorTypeInterface)
            {
                EditorTypes[interface.name] = callback;
            }
            else
                throw "regist edit type error";
        };
        this.setEditType = function(EditorType)
        {

        }

    };
