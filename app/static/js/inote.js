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
        getHTML : function(){
            throw "inote editor exception: function need override.";
        },
        setKeyEvent : function(callback){
            throw "inote editor exception: function need override.";
        }
    };

    var NoteSingleton= function(){};
    NoteSingleton.prototype = {
         getInstanceNames:function(){
            NoteSingleton.names = NoteSingleton.names || new Array;
            return NoteSingleton.names;
         },
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
            NoteSingleton.names = NoteSingleton.names || new Array;
            if(instance instanceof EditorTypeInterface)
            {
                if (instance.editor_name == undefined)
                    throw "inote editor exception: editor_name cannot undefined.";
                NoteSingleton.names.push(instance.editor_name);
                NoteSingleton.instance[instance.editor_name]=instance;
            }
         }
    };

    var noteSingleton = new NoteSingleton;

    /**
    * Note Class
    */

     function Note(NoteId,CateId,EditorType){
        var instance = null;
        var note_id = NoteId;
        var cate_id = CateId;
        var editor_type = EditorType;
        var note_title = "";
        var note_content = "";
        var note_tags = new Array;
        var create_datetime = "";
        var last_modify_datetime = "";

        var get_note = function(){
            $.ajax({
                type:'get',
                url:"note",
                data:{
                    'note_id':note_id,
                },
                dataType: "json",
                contentType: "application/json",
                success:function(data){
//                    console.log('get note:',data)
                    setTitle(data.note_title);
                    setContent(data.note_content);
                    setId(data.note_id);
                    setTags(data.tags);
                }
            });
        };
        var isNew = function(){
            if (getId() == '-1')
                return true;
            else
                return false;
        };
        var save = function(){
                console.log('Save: ');
            if(isNew())
                put();
            else
                update();
        };
        var save_key = function(e){
            if(e)
                if (e.ctrlKey && e.keyCode==83)
                {// Ctrl + S

                    save();

                    e.returnValue=false;
                }

        };
        var init = function(){
            $("#note").remove();
            var note = $('<div id="note" note-id="-1"></div>');
            note.append('<div id="note-title"><input name="noteTitle" id="noteTitle" value placeholder="无标题" tabindex="1" style="width:100%;"></div>');
            note.append('<div id="note-tag"><input name="noteTag" id="noteTag"></div>')
            $("#content").append(note);

            if( editor_type != undefined && editor_type !=null)
            {
                instance = noteSingleton.getInstance(editor_type);
                note.append(instance.getHTML());
                instance.setKeyEvent(save);
                instance.construct();
            }
            note.append('<div id="note-status-bar"></div>');
            // bind quick key
            document.onkeydown = save_key;

            if( note_id != undefined && note_id !=null)
            {
                get_note();
            }
        };
        var put = function(){
            $.ajax({
                type:'put',
                url:"note",
                data:JSON.stringify({
                    'cate_id':cate_id,
                    'note_title':getTitle(),
                    'note_content':getContent(),
                    'note_editor':editor_type,
                    'note_use_tags':getTags(),
                }),
                dataType: "json",
                contentType: "application/json",
                success:function(data){
                    setId(data.note_id);
                    var list = new INote_list("#items", cate_id);
				    list.init();
                }
            });
        };
        var post = function(obj){
            $.ajax({
                type:obj.type,
                url:"note",
                data:obj.data,
                dataType: "json",
                contentType: "application/json",
                success:obj.success,
            });
        };
        var title_update = function(){
            if(note_title != getTitle())
            post({
                type:'post',
                data:JSON.stringify({
                    'type':'modify title',
                    'note_id':getId(),
                    'new_note_title':getTitle(),
                }),
                success:function(data){
                    note_title = getTitle();
                }
            });
        };
        var content_update = function(){
            if(note_content != getContent())
            post({
                type:'post',
                data:JSON.stringify({
                    'type':'modify content',
                    'note_id':getId(),
                    'new_note_content':getContent(),
                }),
                success:function(data){
                    note_content = getContent();
                }
            });
        };
        var tags_update = function(){
            if(note_tags.toString() != getTags().toString())
            post({
                type:'post',
                data:JSON.stringify({
                    'type':'modify tags',
                    'note_id':getId(),
                    'new_note_tags':getTags(),
                }),
                success:function(data){
                    note_tags = getTags();
                }
            });
        };
        var update = function(){
            title_update();
            content_update();
            tags_update();
        };
        var setTitle = function(title){
            note_title = title;
            $("#noteTitle").val(title);
        };
        var getTitle = function(){
            return $("#noteTitle").val();
        };
        var setContent = function(data){
            note_content = data;
            instance.setData(data);
        };
        var getContent = function(){
            return instance.getData();
        };
        var setId = function(id){
            note_id = id;
            $('#note').attr('note-id',id);
        };
        var getId = function(){
            return $('#note').attr('note-id');
        };
        var setTags = function(tags){
            note_tags = tags;
            var title = '';
            for(var i = 0; i< tags.length;i++){
                title+=tags[i].tag_name + ';';
            }
            $("#noteTag").val(title);
        };
        var getTags = function(tags){
            var title = $("#noteTag").val();
            if (title.substring(title.length-1) == ';')
                title = title.substring(0,title.length-1)
            var tags = title.split(';');
            return tags;
        };
        var destruct = function(){
            $('#note').remove();
        };
        return {
            init : init,
            put : put,
            post : post,
            setTitle : setTitle,
            getTitle : getTitle,
            getId : getId,
            setContent : setContent,
            getContent : getContent,
            destruct : destruct,
            update : update,
        };
    };

