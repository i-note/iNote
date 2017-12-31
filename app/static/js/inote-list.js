function INote_list(pos_id,category_id){
    var list_name = "note-list";
    var key = pos_id;
    var id = category_id;

    var addItem = function(id,title,content,img){
        var newItem = $('<div id="note-item " class="note-items item" inote-id='+ id +'> </div>');
        newItem.append('<span class="item-title">' + title + '</span>');
        newItem.append('<div class="item-body" ><span class="item-content-view">' + content + '</span></div>');
        if(img)
            newItem.append('<span class="item-body-right" ><img class="item-image-view" src="' + img + '" alt="test"></span> ');
        $("#note-list").append(newItem);
        newItem.click(function(){
            $(this).addClass("item-active");
            $(this).siblings().removeClass("item-active");
            console.log($(this).attr('inote-id'));

            resetEditor();
        });
    };
    var get_list = function(){
        $.ajax({
            type:'get',
            url:"notelist",
            data:{
                'cate_id':-1,
            },
            dataType: "json",
            contentType: "application/json",
            success:function(data){
                console.log('notelist:',data)
                for (var i=0;i<data.length;i++)
                {
                    addItem(data[i].note_id,data[i].note_title,data[i].note_content);
                }
            }
        });

    };
    var init = function(){
        $("#" + list_name).remove();
        $(key).append('<div id="note-list" class="note-list">');
//        this.addItem(0,"test","hello world"," https://leanote.com/api/file/getImage?fileId=59d5102bab644101ff0021ab");
//        this.addItem(1,"test","hello world","");
//        this.addItem(2,"test","hello world");
        get_list();
        return this;
    };
    var resetEditor = function(){
        $("#note").remove();

        var note = $('<div id="note"></div>');
        note.append('<div id="note-title"><input name="noteTitle" id="noteTitle" value placeholder="无标题" tabindex="1" style="width:100%;"></div>');
        note.append('<div id="note-tag"><input name="noteTag"></div>')

        $("#content").append(note);

        note.append('<div id="note-editor"><textarea id="ckeditor" tabindex="2">test</textarea></div>');
        note.append('<div id="note-status-bar"></div>');
        ReLoadCkeditor();

    };

    return {
        resetEditor:resetEditor,
        init:init,
        addItem:addItem,
        get_list:get_list,
    };
}