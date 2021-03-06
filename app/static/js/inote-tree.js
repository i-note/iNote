
	function lazyLoad(event, data) {
		//console.log("category/"+data.node.key)
		data.result = $.getJSON({
                url:"category",
                data:{'id':data.node.key},
            });
	}

	function loadError(e,data) {
		var error = data.error;
		if (error.status && error.statusText) {
			data.message = "Ajax error: " + data.message;
			data.details = "Ajax error: " + error.statusText + ", status code = " + error.status;
		} else {
			data.message = "Custom error: " + data.message;
			data.details = "An error occurred during loading: " + error;
		}
	}
    var hasnew = false;
    var parent_key = -1;
    var old_parent = undefined;
	$(function(){
		$("#tree").fancytree({
			extensions: ["dnd5","edit","contextMenu"],
			source: $.getJSON({
                url:"category",
                data:{'id':'-1'},
            }),
			contextMenu: {
				menu: {
					"add": { "name": "Add", "icon": "add" },
					"rename": { "name": "Rename", "icon": "edit" },
					"delete": { "name": "Delete", "icon": "delete" },
					"sep1": "---------",
					"reload": { "name": "Reload", "icon": "reload" },
					"sep2": "---------",
					"public": {
						"name": "Public",
						"items": {
							"public_as_blog": { "name": "Public as blog" },
							"cancel_public": { "name": "Cancel public" },
						}
					},
					"share": {
						"name": "Share",
						"items": {
							"share_to_qq": { "name": "QQ" },
							"share_to_wechat": { "name": "wechat" },
							"share_to_sina": { "name": "sina" }
						}
					}
				},
				actions: function(node, action, options) {
					//console.log("Selected '" + action + "' on " + node);
					if (action == 'add') {
						// add
						hasnew = true;
						var node = $("#tree").fancytree("getActiveNode");
						parent_key = node.key;
						node.editCreateNode("child", "new category");
					}else if (action == 'delete') {
						// delete
                        var node = $("#tree").fancytree("getActiveNode");

                            $.post({
                                type:'delete',
                                url:"category",
                                data:JSON.stringify({
                                    'cate_id':node.key,
                                }),
                                dataType: "json",
                                contentType: "application/json",
                                success:function(data){
                                    if(data.status == 'success')
                                        node.remove();
                                }
                            });

					}else if (action == 'rename') {
						// rename
                        $('#'+$("#tree").fancytree("getActiveNode").li.id).dblclick();
					}
				}
			},

			ajax: { debugDelay: 1000 },
			lazyLoad: lazyLoad,
			loadError: loadError,

			createNode: function(event, data) {
			},
			modifyChild: function(event, data) {
			},
			focus: function(event, data) {
			},
			keydown: function(event, data) {
				//console.log('keydown: ',event.which);
				switch( event.which ) {
					case 32: // [space]
						data.node.toggleSelected();
						break;
					case 46: // [delete]
						var node = $("#tree").fancytree("getActiveNode");

						    $.post({
                                type:'delete',
                                url:"category",
                                data:JSON.stringify({
                                    'cate_id':node.key,
                                }),
                                dataType: "json",
                                contentType: "application/json",
                                success:function(data){
                                    if(data.status == 'success')
                                        node.remove();
                                }
                            });
						break;
					case 116: // [F5]

						break;
					case 78: // [n]
						data.node;
						break;
				}
				return false;
			},
			dnd5: {
				dragStart: function(node, data) {
				    //old_parent = node.parent;
				    node.old_expanded = node.isExpanded();
				    node.setExpanded(false);
					return true;
				},
				dragDrag: function(node, data) {
					data.dataTransfer.dropEffect = "move";
				},
				dragEnd: function(node, data) {
				},
				dragEnter: function(node, data) {
					data.dataTransfer.dropEffect = "move";
					node.enter='enter'
					return true;
				},
				dragOver: function(node, data) {
					data.dataTransfer.dropEffect = "move";
				},
				dragLeave: function(node, data) {
					data.dataTransfer.dropEffect = "copy";
				},
				dragDrop: function(node, data) {
					var transfer = data.dataTransfer;
					if( data.otherNode ) {
					    var hasChange = false;
					    var current_node_key = data.otherNode.key;
					    var parent_node_key = -1;
					    if(data.hitMode=='over')
					    {
					        console.log(node.title,' will is ',data.otherNode.title,"'s parent");
					        hasChange = true;

                            parent_node_key = node.key;
					    }else{
					        if(node.parent != data.otherNode.parent){
					            console.log(node.title,' will is ',data.otherNode.title,"'s sibling");
					            hasChange = true;

					            if(node.parent.parent != null)
                                    parent_node_key = node.parent.key;
					        }
					    }
						if(hasChange){
						    hasChange=false;
						    var current_node = data.otherNode;

						    $.ajax({
                                type:'put',
                                url:"category",
                                data:JSON.stringify({
                                    'type':'move to',
                                    'current_cate_id':current_node_key,
                                    'dest_parent_cate_id':parent_node_key
                                }),
                                dataType: "json",
                                contentType: "application/json",
                                success:function(data){
                                    if(data.status == 'success'){
                                        console.log('move to: successful')
                                        current_node.moveTo(node, data.hitMode);
                                        current_node.setExpanded(current_node.old_expanded);
                                        //node.render()
                                    }
                                    else{
                                        console.log('move to: ',data.status)
                                        current_node.setExpanded(current_node.old_expanded);
                                    }
                                }
                            });



						}
					} else if( data.otherNodeData ) {
						node.addChild(data.otherNodeData, data.hitMode);
					} else {
						node.addNode({
							title: transfer.getData("text")
						}, data.hitMode);
					}
					node.setExpanded(node.old_expanded);
				}
			},
			edit: {
				triggerStart: ["f2", "dblclick", "shift+click", "mac+enter"],
				beforeEdit: function(event, data){
				},
                edit: function(event, data){
                },
                beforeClose: function(event, data){
                    console.log(event.type, event, data);
                    if( data.originalEvent.type === "mousedown" ) {
                    }
                },
                save: function(event, data){
                    old_title = data.node.title;
                    current_node = data.node;
                    setTimeout(function(){
                        if(hasnew){
                        //new category
                            hasnew = false;
                            $.post({
                                type:'post',
                                url:"category",
                                data:JSON.stringify({
                                    'parent_cate_id':parent_key,
                                    'new_cate_title':current_node.title
                                }),
                                dataType: "json",
                                contentType: "application/json",
                                success:function(data){
                                    if(data)
                                        current_node.key = data.id;
                                }
                            });
                        }else{
                        // rename category
                            $.ajax({
                                type:'put',
                                url:"category",
                                data:JSON.stringify({
                                    'type':'rename',
                                    'id':current_node.key,
                                    'new_cate_title':current_node.title
                                }),
                                dataType: "json",
                                contentType: "application/json",
                                success:function(data){
                                    if(data.status == 'success'){
                                        console.log('rename: successful')
                                    }
                                    else if(data.status == 'permission denied'){
                                        current_node.setTitle(old_title);
                                    }
                                    else if(data.status == 'cannot changed'){
                                        current_node.setTitle(old_title);
                                    }
                                    else if(data.status == 'resource not found'){
                                        current_node.setTitle(old_title);
                                    }
                                }
                            });
                        }

                        $(data.node.span).removeClass("pending");
                    }, 2000);
                    return true;
                },
                close: function(event, data){
                    if( data.save ) {
                        $(data.node.span).addClass("pending");
                    }
                }
			},
			activate: function(event, data) {
				var list = new INote_list("#items",data.node.key);
				console.log(list.id);
				list.init();
			},
			tooltip: function(event, data) {
				return data.node.title;
			},
			icon: function(event, data) {
				var node = data.node;
				if( node.data.children === null ) {
					return "foo-icon-class";
			    }
			},
		});
	});

function get_cur_cate_id(){
    var node = $("#tree").fancytree("getActiveNode");
    if(node)
        return node.key;
    else
        return null;
}