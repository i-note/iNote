
    function ReLoadCkeditor(save)
    {
        var ck_editor = CKEDITOR.replace('ckeditor');
        ck_editor.on('instanceReady',function(event)                  //准备
        {
            var editor=event.editor;
            setTimeout(function()
                {     //延时加载
                   if(!editor.element)
                   {
                        setTimeout(arguments.callee,1);
                        return;
                   }
                   event.removeListener('instanceReady',this.callee);
                   if(editor.name=='ckeditor')
                   {
                        var che_find = $("#cke_ckeditor")[0].classList[0];
                        var height = $(window).height()- $("#"+che_find+"_top").position().top - $("#"+che_find+"_top").outerHeight(true) - $("#"+che_find+"_bottom").outerHeight(true) - 2 ;
                        $('#'+che_find+'_contents').height(height);
                   }

                    document.getElementsByTagName('iframe')[0].contentDocument.getElementsByTagName('body')[0].onkeydown=function(e){
                        if (e.ctrlKey && e.key=='s')
                        {// Ctrl + S
                            save();

                            e.returnValue=false;
                        }

                    };
                },0);
        },null,null,9999);
        $(window).resize(function () {
            var che_find = $("#cke_ckeditor")[0].classList[0];
            var height = $(window).height()- $("#"+che_find+"_top").position().top - $("#"+che_find+"_top").outerHeight(true) - $("#"+che_find+"_bottom").outerHeight(true) - 2;
            $('#'+che_find+'_contents').height(height);


        });
        return ck_editor;
    }
//    $('#ckeditor').ready(ReLoadCkeditor);

    var Inote_CKEditor = function(name){
        var editor = null;
        var keydown = null;
        if(!name)
            this.editor_name =  "ckeditor";
        else
            this.editor_name = name;
//        console.log(this.editor_name)

        this.construct=function(){
            editor = ReLoadCkeditor(keydown);
        }
        this.destruct=function(){
            console.log("test");
        }
        this.getData=function(){
            return editor.getData();
        }
        this.setData=function(data){
            var __editor = editor;
            setTimeout(function()
                {     //延时加载
                    __editor.setData(data);
                },null,null,10);
        }
        this.getHTML=function(){
            return '<div id="note-editor"><textarea id="ckeditor" tabindex="2"></textarea></div>';
        }
        this.setKeyEvent=function(callback){
            keydown = callback;
        }

    };

    Inote_CKEditor.prototype = new EditorTypeInterface;
    noteSingleton.addInstance(new Inote_CKEditor);


