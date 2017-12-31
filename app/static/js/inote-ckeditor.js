
    function ReLoadCkeditor()
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
                },0);
        },null,null,9999);
        $(window).resize(function () {
            var che_find = $("#cke_ckeditor")[0].classList[0];
            var height = $(window).height()- $("#"+che_find+"_top").position().top - $("#"+che_find+"_top").outerHeight(true) - $("#"+che_find+"_bottom").outerHeight(true) - 2;
            $('#'+che_find+'_contents').height(height);
        });
    }
    $('#ckeditor').ready(ReLoadCkeditor);

    var Inote_CKEditor = function(name){
        if(!name)
            this.editor_name =  "ckeditor";
        else
            this.editor_name = name;
        console.log(this.editor_name)

        this.construct=function(){

            ReLoadCkeditor();
        }
        this.destruct=function(){
            console.log("test");
        }
        this.getData=function(){
            console.log("test");
        }
        this.setData=function(data){

        }

    };


    Inote_CKEditor.prototype = new EditorTypeInterface;
    note.addInstance(new Inote_CKEditor);