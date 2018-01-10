
function INote_list(pos_id,CateId){
    var list_name = "note-list";
    var key = pos_id;
    var cate_id = CateId;

    var addItem = function(id,title,note_edit_type,content,img){
        var newItem = $('<div id="note-item " class="note-items item" inote-id='+ id +' inote_edit_type='+note_edit_type+'> </div>');
        newItem.append('<span class="item-title">' + title + '</span>');
        newItem.append('<div class="item-body" ><span class="item-content-view">' + content + '</span></div>');
        if(img)
            newItem.append('<span class="item-body-right" ><img class="item-image-view" src="' + img + '" alt="test"></span> ');
        $("#note-list").append(newItem);
        newItem.click(function(){
            $(this).addClass("item-active");
            $(this).siblings().removeClass("item-active");

            resetEditor($(this).attr('inote-id'),$(this).attr('inote_edit_type'));
        });

            $.contextMenu({
                selector: '.note-items',
                callback: function(key, options) {
                    var item = $(options.$trigger.context);
                    if(key == 'edit'){
                        resetEditor(item.attr('inote-id'),item.attr('inote_edit_type'));
                    }else if(key == 'delete')
                    {
                        remove(item);
                    }
                },
                items: {
                    "edit": {name: "Edit", icon: "edit"},
                    "cut": {name: "Cut", icon: "cut"},
                    "copy": {name: "Copy", icon: "copy"},
                    "paste": {name: "Paste", icon: "paste"},
                    "delete": {name: "Delete", icon: "delete"},
                    "sep1": "---------",
                    "quit": {name: "Quit", icon: "quit"}
                }
            });

    };
    var remove = function(item){
        var note_id = item.attr('inote-id');
        new Note().post({
            'type':'delete',
            data:JSON.stringify({
                'note_id':note_id
            }),
            success:function(data){
                if(data.status == 'success'){
                    item.remove();
                    if(note_id == note.getId())
                        note.destruct();
                }else if(data.status == 'resource not found'){

                }
            }
        });
    };

    var get_list = function(){
        $.ajax({
            type:'get',
            url:"notelist",
            data:{
                'cate_id':cate_id,
            },
            dataType: "json",
            contentType: "application/json",
            success:function(data){
                console.log('notelist: ',data)
                for (var i=0;i<data.length;i++)
                {
                    addItem(data[i].note_id,data[i].note_title,data[i].note_edit_type,data[i].note_content);
                }
            }
        });
    };

    var init = function(){
        $("#" + list_name).remove();
        $(key).append('<div id="note-list" class="note-list">');
//        this.addItem(0,"test","hello world"," https://leanote.com/api/file/getImage?fileId=59d5102bab644101ff0021ab");

        get_list();
        return this;
    };

    var resetEditor = function(note_id, editor_type){
        note = new Note(note_id, cate_id , editor_type);
        note.init();
    };

    return {
        resetEditor:resetEditor,
        init:init,
        addItem:addItem,
        get_list:get_list,
    };
}