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
        var title = "";
        var content = "";
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
            return true;
        };
        var save = function(){
                console.log('Save: ');
            if(isNew)
                put();
            else
                post();
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
                }
            });
        };
        var post = function(){
            $.ajax({
                type:'post',
                url:"note",
                data:JSON.stringify({
                    'cate_id':getId(),
                    'note_title':getTitle(),
                    'note_content':getContent(),
                    'note_editor':editor_type,
                    'note_use_tags':getTags(),
                }),
                dataType: "json",
                contentType: "application/json",
                success:function(data){
                    if(data.status == 'success'){
                        console.log('rename: successful; ', data);
                    }
                }
            });
        };
        var setTitle = function(title){
            console.log('title',title);
            $("#noteTitle").val(title);
        };
        var getTitle = function(){
            return $("#noteTitle").val();
        };
        var setContent = function(data){
            instance.setData(data);
        };
        var getContent = function(){
            return instance.getData();
        };
        var setId = function(id){
            $('#note').attr('note-id',id);
        };
        var getId = function(){
            return $('#note').attr('note-id');
        };
        var setTags = function(tags){
            var title = '';
            for(var i = 0; i< tags.length;i++){
                title+=tags[i].tag_name + ';';
            }
            $("#noteTag").val(title);
        };
        var getTags = function(tags){
            var title = $("#noteTag").val();
            var tags = title.split(';');
            return tags;
        };
        return {
            init : init,
            put : put,
            post : post,
            setTitle : setTitle,
            getTitle : getTitle,
            setContent : setContent,
            getContent : getContent,
        };
    };

