
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
                        var height = $(window).height()- $("#cke_1_top").position().top - $("#cke_1_top").outerHeight(true) - $("#cke_1_bottom").outerHeight(true) - 2 ;
                        $('#cke_1_contents').height(height);
                   }
                },0);
        },null,null,9999);
        $(window).resize(function () {
            var height = $(window).height()- $("#cke_1_top").position().top - $("#cke_1_top").outerHeight(true) - $("#cke_1_bottom").outerHeight(true) - 2;
            $('#cke_1_contents').height(height);
        });
    }
    $('#ckeditor').ready(ReLoadCkeditor);
    <!--ReLoadCkeditor()-->
        <!--//赋值-->
        <!--ckeditor.setData("content");-->
        <!--//获取源码-->
        <!--ckeditor.getData();-->
