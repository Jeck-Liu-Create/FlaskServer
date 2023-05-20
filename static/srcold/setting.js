 $("#sel_exportoption").change(function () {
        //刷新参数设置
        $('#tabledata').bootstrapTable('refreshOptions', {
            exportDataType: $(this).val()
        });
    });

//返回开始时间
    function StartTime()
    {
        var now = new Date();

        var year = now.getFullYear();       //年
        var month = now.getMonth() + 1;     //月
        var day = now.getDate();            //日


        var clock = year + "-";

        if(month < 10)
            clock += "0";

        clock += month + "-";

        if(day < 10)
            clock += "0";

        clock += day + "T";

        clock += "00:00:00";
        return(clock);
    }
//返回结束日期
    function EndTime()
    {
        var now = new Date();

        var year = now.getFullYear();       //年
        var month = now.getMonth() + 1;     //月
        var day = now.getDate();            //日

        var hh = now.getHours();            //时
        var mm = now.getMinutes();          //分
        var ss = now.getSeconds() ;         //秒


        var clock = year + "-";

        if(month < 10)
            clock += "0";

        clock += month + "-";

        if(day < 10)
            clock += "0";

        clock += day + "T";

        if(hh < 10)
            clock += "0";

        clock += hh + ":";

        if (mm < 10)
            clock += '0';

        clock += mm + ":";

        if (ss < 10)
            clock += '0';

        clock += ss ;

        return(clock);
    }
    //时间初始化
    $(function(){

       $('#s_time').val(StartTime())
    });
    $(function(){

       $('#e_time').val(EndTime())
    });

    function updata() {
        console.log("Search_roll_nm="+$("#Search_roll_nm").val());
        var ROLL_NM = '';
        var str = $("#Search_roll_nm").val();
        if (str === '' || str === undefined || str == null) {
            //return true;
            console.log('空');
            ROLL_NM = 'null';
        } else {
            //return false;
            console.log('非空');
            ROLL_NM = str;
        }
	    $('#tabledata').bootstrapTable({
        url:'/reload',
        queryParams : function(params) {
				return {
					limit: params.limit,
					offset: params.offset,
	               // userName: $.trim( $('#userName').val() ) ,
	               // age: $.trim( $('#age').val() ) ,
                    ROLL:$('#roll').val(),
                    StartTime:$('#s_time').val(),
                    EndTime:$('#e_time').val(),
                    ROLLNM:ROLL_NM,
				}
			},
		toolbar:'#toolbox',
        fixedColumns: true,
        fixedNumber: 2,
        pagination: true, //前端处理分页
        singleSelect: false, //是否只能单选
        cache: true, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pageNumber: 1, //初始化加载第10页，默认第一页
        pageSize: 10, //每页的记录行数（*）
        pageList: [5, 10, 20, 50, 100], //可供选择的每页的行数（*）
		clickToSelect:true,
		sortName: "create_time",
		sortOrder: "desc",
        showColumns: true, //显示内容列下拉框
        minimumCountColumns: 2, //当列数小于此值时，将隐藏内容列下拉框
        uniqueId: "id", //每一行的唯一标识，一般为主键列
        showToggle: true, //是否显示详细视图和列表视图的切换按钮
        cardView: false, //是否显示详细视图
       // queryParamsType:'limit',
        sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
        showExport: true, //导出按钮
        exportDataType: "selected", //导出表格方式（默认basic：只导出当前页的表格数据；all：导出所有数据；selected：导出选中的数据）
        exportTypes: ['json', 'xml', 'csv', 'txt', 'sql', 'excel'], //导出文件类型
        exportOptions: {
            // 导出数据去除第一列出现"on"
            ignoreColumn: [0,1,28,32,33,34]
        },
		columns: [{
            //#0 选择
                checkbox: true,
                visible: true,
            },{
            //#1 操作
                title: '操作',
                field: 'c_id',
                align: 'center',
                formatter: actionFormatter
            },{
            //#2 序号
                field: 'number',
                title: '序号',
                align: 'center'
            }, {
            //#3 机架号
                field: 'c_frame_id',
                title: '机架号',
                align: 'center',
            }, {
            //#4 轧辊号
                field: 'c_roll_number',
                title: '辊号',
                align: 'center'
            }, {
            //#6 轧辊位置
                field: 'c_roll_position',
                title: '轧辊位置',
                align: 'center',
            }, {
            //#7 磨前直径
                field: 'c_diameter_before',
                title: '磨前直径',
                align: 'center',
            }, {
            //#8 磨后直径
                field: 'c_diameter',
                title: '磨后直径',
                align: 'center',
            }, {
            //#9 磨削量
                field: 'c_grinding_amount',
                title: '磨削量',
                align: 'center',
                visible: true,
            }, {
            //#10 曲线
                field: 'c_curve',
                title: '曲线',
                align: 'center',
            }, {
            //#11 凸度值 c_crown_value
                field: 'c_crown_value',
                title: '凸度值',
                align: 'center',
            }, {
            //#12 凸度正负标记
                field: 'c_crown_symbol',
                title: '凸度正负标记',
                align: 'center',
            }, {
            //#13 圆度
                field: 'c_roundness',
                title: '圆度',
                align: 'center',
            }, {
            //#14 圆柱度
                field: 'c_cylindricity',
                title: '圆柱度',
                align: 'center',
            }, {
            //#15 同轴度
                field: 'c_coaxiality',
                title: '同轴度',
                align: 'center',
            }, {
            //#16 粗糙度
                field: 'c_roughness',
                title: '粗糙度',
                align: 'center',
            }, {
            //#17 误差
                field: 'c_error',
                title: '误差',
                align: 'center',
            }, {
            //#19 磨削原因
                field: 'c_cause',
                title: '磨削原因',
                align: 'center',
            }, {
            //#20 探伤结果
                field: 'c_result_detection',
                title: '探伤结果',
                align: 'center',
            }, {
            //#21 配对轧辊号
                field: 'c_pairing_roll',
                title: '配对辊号',
                align: 'center'
            }, {
            //#22 日期
                field: 'c_date',
                title: '日期',
                align: 'center',
            }, {
            //#23 操作者
                field: 'c_operator',
                title: '操作者',
                align: 'center',
                visible: true,
            }, {
            //#24 砂轮直径
                field: 'c_wheel_diameter',
                title: '砂轮直径',
                align: 'center',
            }, {
            //#25 轧辊材质
                field: 'c_roll_material',
                title: '轧辊材质',
                align: 'center',
            }, {
            //#26 轧辊类型
                field: 'c_roll_type',
                title: '轧辊类型',
                align: 'center',
            }, {
            //#27 驱动侧轴承号
                field: 'c_drive_bearing',
                title: '驱动侧轴承号',
                align: 'center',
            }, {
            //#28 操作侧轴承号
                field: 'c_side_bearing',
                title: '操作侧轴承号',
                align: 'center',
            }, {
            //#29 开始时间
                field: 'c_start_time',
                title: '开始时间',
                align: 'center',
            }, {
            //#30 结束时间
                field: 'c_end_time',
                title: '结束时间',
                align: 'center',
            }, {
            //#31 磨床
                field: 'c_grinding_machine',
                title: '磨床',
                align: 'center',
                visible: false
            }, {
            //#32 锥形顶端直径
                field: 'c_top_diameter',
                title: '锥形顶端直径',
                align: 'center',
            }, {
            //#33 锥形底端直径
                field: 'c_low_diameter',
                title: '锥形底端直径',
                align: 'center',
            }, {
            //#34 实际凸度 c_actual_convexity
                field: 'c_actual_convexity',
                title: '实际凸度',
                align: 'center',
            }, {
            //#35 班次c_shift
                field: 'c_shift',
                title: '班次',
                align: 'center',
                visible: false
            }, {
            //#36 程序号c_program_number
                field: 'c_shift',
                title: '程序号',
                align: 'center',
                visible: false
            }, {
            //#37
                field: 'c_id',
                title: 'ID',
                visible:false,
                align: 'center',
        },{
            //#38
                field: 'c_woolification',
                title: '是否毛化标记',
                visible:false,
                align: 'center',
        }
        ],
        onLoadSuccess: function (){
        },
        onLoadError: function (){
            showTips("数据加载失败！");
        },
        onDblClickRow: function ( row ) {
            var list = [row.c_id,row.c_roll_number,row.c_diameter,row.c_frame_id,row.c_roll_type,row.c_roll_position,row.c_roll_material,row.c_crown_symbol,row.c_roughness,row.c_side_bearing,row.c_drive_bearing,row.c_pairing_roll,row.c_top_diameter,row.c_low_diameter,row.number,row.c_cause,row.c_result_detection,row.c_crown_value];
            console.log(list);
            EditViewById(list);
        }

    });

    }

    function actionFormatter( value, row) {
        var result = "";
        // list = [ [0]ID , [1]轧辊号 ， [2]直径  ， [3]机架号 ，[4]轧辊类型 ，[5]轧辊位置 ，[6]轧辊材质 ， [7]凸度正负标记 ， [8]粗糙度， [9]操作侧轴承号 ， [10]驱动侧轴承号 ， [11]配对辊号 ， [12]锥形顶端直径 ， [13]锥形底端直径 ， [14]索引, [15]磨削原因， [16]探伤结果, [17]凸度值 ]
        var list = [row.c_id,row.c_roll_number,row.c_diameter,row.c_frame_id,row.c_roll_type,row.c_roll_position,row.c_roll_material,row.c_crown_symbol,row.c_roughness,row.c_side_bearing,row.c_drive_bearing,row.c_pairing_roll,row.c_top_diameter,row.c_low_diameter,row.number,row.c_cause,row.c_result_detection,row.c_crown_value];
        result += "<a href='javascript:;' class='btn btn-xs blue' onclick=\"EditViewById('" + list + "')\" title='编辑'><span class='glyphicon glyphicon-pencil'></span></a>";
        return result;
    }

    function EditViewById(data){
        console.log(data);
        if (typeof data == 'string')
        {
            console.log('字符串类型')
            row = data.split(",");
        }
        else
        {
            console.log('列表类型')
            row = data;
        }
        console.log('执行的数据'+row);
        // console.log(typeof(row[1]));
        // var row = $("tabledata").bootstrapTable('getData',false);
        $("#modal_c_id").val(row[0]);//数据库ID
        $("#modal_c_roll_number").val(row[1]);//轧辊编号
        $("#modal_c_diameter").val(row[2]);//直径
        $("#modal_c_frame_id").val(row[3]);//机架号
        $("#modal_c_roll_type").val(row[4]);//轧辊类型
        $("#modal_c_roll_position").val(row[5]);//轧辊位置
        // $("#modal_c_roll_material").val(row[6]);//轧辊材质
        if (row[6]===null || row[6]==='')
        {
            console.log(typeof row[6] +  row[6] + "空");
            $("#modal_c_roll_material").val("05:MC5");//凸度值
        }else {
            console.log(typeof row[6] +  row[6] + "非空");
            $("#modal_c_roll_material").val(row[6]);//凸度值
        }

        // $("#modal_c_crown_symbol").val(row[7]);//凸度正负标记
        if (row[7]===null || row[7]==='')
        {
            console.log(typeof row[7] +  row[7] + "空");
            $("#modal_c_crown_symbol").val("2:正");//凸度值
        }else {
            console.log(typeof row[7] +  row[7] + "非空");
            $("#modal_c_crown_symbol").val(row[7]);//凸度值
        }

        $("#modal_c_roughness").val(row[8]);//粗糙度
        $("#modal_c_side_bearing").val(row[9]);//操作侧轴承号
        $("#modal_c_drive_bearing").val(row[10]);//驱动侧轴程号
        $("#modal_c_pairing_roll").val(row[11]);//配对辊号
        // $("#modal_c_top_diameter").val(row[12]);//锥形顶端直径
        if (row[12]===null || row[12]==='')
        {
            console.log(typeof row[12] +  row[12] + "空");
            $("#modal_c_top_diameter").val("0000000");//凸度值
        }else {
            console.log(typeof row[12] +  row[12] + "非空");
            $("#modal_c_top_diameter").val(row[12]);//凸度值
        }

        // $("#modal_c_low_diameter").val(row[13]);//锥形底端直径
        if (row[13]===null || row[13]==='')
        {
            console.log(typeof row[13] +  row[13] + "空");
            $("#modal_c_low_diameter").val("0000000");//凸度值
        }else {
            console.log(typeof row[13] +  row[13] + "非空");
            $("#modal_c_low_diameter").val(row[13]);//凸度值
        }

        $("#modal_index").val(row[14]);//index
        $("#modal_c_cause").val(row[15]);//磨削原因
        // $("#modal_c_result_detection").val(row[16]);//探伤结果
        if (row[16]===null || row[16]==='')
        {
            console.log(typeof row[16] +  row[16] + "空");
            $("#modal_c_result_detection").val("裂纹探伤结果：\n软点探伤结果：");//凸度值
        }else {
            console.log(typeof row[16] +  row[16] + "非空");
            $("#modal_c_result_detection").val(row[16]);//凸度值
        }


        if (row[17]===null || row[17]==='')
        {
            console.log(typeof row[17] +  row[17] + "空");
            $("#modal_c_crown_value").val("0000");//凸度值
        }else {
            console.log(typeof row[17] +  row[17] + "非空");
            $("#modal_c_crown_value").val(row[17]);//凸度值
        }

        $("#myModal").modal();
        check_c_diameter();
        check_c_crown();
        check_c_roughness();
        check_c_side_bearing();
        check_c_drive_bearing();
        check_c_pairing_roll();
        check_c_top_diameter();
        check_c_low_diameter();
        check_c_frame_id();
        check_c_roll_type();
        check_c_roll_position();
        check_c_roll_material();
        check_c_crown_symbol();

        $('#send-btn').attr('disabled','disabled')

    }



    $(function (){updata()})
    //搜索按钮
    $('#send').click(function(){
        $("#tabledata").bootstrapTable('destroy');

        updata();

    });

    $('#demo').click(function (){
        var show = $('#modal_send').css('display');
        if ( show == 'block')
        {
            $('#modal_send').attr("style","display:none")
            $('#modal_one').attr("style","display:none")
            $('#modal_tow').attr("style","display:none")
            $('#modal_three').attr("style","display:none")
            $('#modal_four').attr("style","display:none")
            $('#modal_c_do').attr("style","display:none")
            $('#modal_five').attr("style","display:none")
            $('#modal_eight').attr("style","display:none")
            $('#modal_other').attr("class","col-sm-8")
        }
        if ( show == 'none')
        {
            $('#modal_send').attr("style","display:block")
            $('#modal_one').attr("style","display:block")
            $('#modal_tow').attr("style","display:block")
            $('#modal_three').attr("style","display:block")
            $('#modal_four').attr("style","display:block")
            $('#modal_c_do').attr("style","display:block")
            $('#modal_five').attr("style","display:block")
            $('#modal_eight').attr("style","display:block")
            $('#modal_other').attr("class","col-sm-3")
        }
    });


    //保存按钮
    $('#sava-edit-btn').click(function() {
        // addmLoading("上传中...");
        var show = $('#modal_send').css('display');
        if (show == 'block') {
            var boolstr_check_c_crown = check_c_crown()
            var boolstr_c_roughness = check_c_roughness()
            var boolstr_c_side_bearing = check_c_side_bearing()
            var boolstr_c_drive_bearing = check_c_drive_bearing()
            var boolstr_c_pairing_roll = check_c_pairing_roll()
            var boolstr_c_top_diameter = check_c_top_diameter()
            var boolstr_c_low_diameter = check_c_low_diameter()
            var boolstr_c_diameter = check_c_diameter()

            var boolstr_c_frame_id = check_c_frame_id()
            var boolstr_c_roll_type = check_c_roll_type()
            var boolstr_c_roll_position = check_c_roll_position()
            var boolstr_c_roll_material = check_c_roll_material()
            var boolstr_c_crown_symbol = check_c_crown_symbol()


            var boolstr = (boolstr_c_diameter && boolstr_check_c_crown && boolstr_c_roughness && boolstr_c_side_bearing && boolstr_c_drive_bearing && boolstr_c_pairing_roll && boolstr_c_top_diameter && boolstr_c_low_diameter && boolstr_c_frame_id && boolstr_c_roll_type && boolstr_c_roll_position && boolstr_c_roll_material && boolstr_c_crown_symbol)
            console.log(boolstr);
            if (boolstr) {
                var c_frame_id = $('#modal_c_frame_id').val();
                var c_roll_type = $('#modal_c_roll_type').val();
                var c_roll_position = $('#modal_c_roll_position').val();
                var c_roll_material = $('#modal_c_roll_material').val();
                var c_diameter = $('#modal_c_diameter').val();
                var c_crown_value = $('#modal_c_crown_value').val();
                var c_crown_symbol = $('#modal_c_crown_symbol').val();
                var c_roughness = $('#modal_c_roughness').val();
                var c_side_bearing = $('#modal_c_side_bearing').val();
                var c_drive_bearing = $('#modal_c_drive_bearing').val();
                var c_id = $('#modal_c_id').val();
                var c_roll_number = $('#modal_c_roll_number').val();
                var c_pairing_roll = $('#modal_c_pairing_roll').val();
                var c_top_diameter = $('#modal_c_top_diameter').val();
                var c_low_diameter = $('#modal_c_low_diameter').val();
                var c_cause = $('#modal_c_cause').val();
                var index = $('#modal_index').val();
                var c_result_detection = $('#modal_c_result_detection').val();
                var data = {
                    data: JSON.stringify({
                        'c_frame_id': c_frame_id,
                        'c_roll_type': c_roll_type,
                        'c_roll_position': c_roll_position,
                        'c_roll_material': c_roll_material,
                        'c_diameter': c_diameter,
                        'c_crown_value': c_crown_value,
                        'c_crown_symbol': c_crown_symbol,
                        'c_roughness': c_roughness,
                        'c_side_bearing': c_side_bearing,
                        'c_drive_bearing': c_drive_bearing,
                        'c_id': c_id,
                        'c_roll_number': c_roll_number,
                        'c_pairing_roll': c_pairing_roll,
                        'c_top_diameter': c_top_diameter,
                        'c_low_diameter': c_low_diameter,
                        'c_cause': c_cause,
                        'c_result_detection': c_result_detection,
                    })
                };
                console.log(data);
                //将编辑数据发送到后台
                $.ajax({
                    type: "POST",
                    url: "/edit",
                    data: data,
                    dataType: "json",
                    success: function (res) {
                        console.log(res);
                        console.log(0)
                        if (res['data'] === '修改成功') {
                            $(function () {
                                console.log('单行更新的index=' + index);
                                $('#tabledata').bootstrapTable('updateRow', {
                                    index: index - 1,               //行索引
                                    row: {
                                        c_frame_id: c_frame_id,
                                        c_roll_type: c_roll_type,
                                        c_roll_position: c_roll_position,
                                        c_roll_material: c_roll_material,
                                        c_crown_symbol: c_crown_symbol,
                                        c_roughness: c_roughness,
                                        c_side_bearing: c_side_bearing,
                                        c_drive_bearing: c_drive_bearing,
                                        c_pairing_roll: c_pairing_roll,
                                        c_top_diameter: c_top_diameter,
                                        c_low_diameter: c_low_diameter,
                                        c_cause: c_cause,
                                        c_result_detection: c_result_detection,
                                        c_crown_value: c_crown_value,
                                    }
                                })
                            })
                            $.message({
                                message: '保存成功',
                                duration: '1000',
                                center: true,
                                type: 'success'
                            });
                            $('#send-btn').removeAttr('disabled')
                        } else {
                            $.message({
                                message: '保存失败',
                                duration: '1000',
                                center: true,
                                type: 'error'
                            });
                        }

                    },
                    error: function (res) {
                        console.log(res);
                        console.log(1);
                        $.message({
                            message: '服务器连接失败',
                            type: 'warning',
                            duration: 0,
                            showClose: true,
                            center: true,
                            onClose: function () {
                                alert('知道了')
                            }
                        });
                    },

                });
                // setTimeout(function(){
                //     clearmLoading();
                // },3000);//300代表延迟毫秒值
            } else {
                $.message({
                    message: '数据不正确',
                    duration: '1000',
                    center: true,
                    type: 'warning',
                    showClose: false,
                });
            }
        } else {
            var boolstr_none = (check_c_diameter() && check_c_roughness() && check_c_pairing_roll());
            console.log(boolstr_none);
            if (boolstr_none) {
                var c_diameter_none = $('#modal_c_diameter').val();
                var c_id_none = $('#modal_c_id').val();
                var index_none = $('#modal_index').val();
                var c_cause_none = $('#modal_c_cause').val();
                var c_result_detection_none = $('#modal_c_result_detection').val();
                var c_roughness_none = $('#modal_c_roughness').val();
                var c_pairing_roll_none = $('#modal_c_pairing_roll').val();
                var data_none = {
                    data: JSON.stringify({
                        'c_diameter_none': c_diameter_none,
                        'c_id_none': c_id_none,
                        'c_cause_none': c_cause_none,
                        'c_result_detection_none': c_result_detection_none,
                        'c_roughness_none': c_roughness_none,
                        'c_pairing_roll_none': c_pairing_roll_none,
                    })
                };
                console.log(data_none);
                $.ajax({
                    type: "POST",
                    url: "/editnone",
                    data: data_none,
                    dataType: "json",
                    success: function (res) {
                        console.log(res);
                        console.log(0)
                        if (res['data'] === '修改成功') {
                            $(function () {
                                console.log('单行更新的index=' + index_none);
                                $('#tabledata').bootstrapTable('updateRow', {
                                    index: index_none - 1,               //行索引
                                    row: {
                                        c_id_none: c_id_none,
                                        c_diameter: c_diameter_none,
                                        c_cause: c_cause_none,
                                        c_result_detection: c_result_detection_none,
                                        c_roughness: c_roughness_none,
                                        c_pairing_roll: c_pairing_roll_none,
                                    }
                                })
                            })
                            $.message({
                                message: '保存成功',
                                duration: '1000',
                                center: true,
                                type: 'success'
                            });
                            $('#send-btn').removeAttr('disabled')
                        } else {
                            $.message({
                                message: '保存失败',
                                duration: '1000',
                                center: true,
                                type: 'error'
                            });
                        }
                    },
                    error: function (res) {
                        console.log(res);
                        console.log(1);
                        $.message({
                            message: '服务器连接失败',
                            type: 'warning',
                            duration: 0,
                            showClose: true,
                            center: true,
                            onClose: function () {
                                alert('知道了')
                            }
                        });
                    },
                });
            } else {
                $.message({
                    message: '数据不正确',
                    duration: '1000',
                    center: true,
                    type: 'warning',
                    showClose: false,
                });
            }
        }
    });


    $('#send-btn').click(function (){
            var c_id = $('#modal_c_id').val();
            var data = {
                data: JSON.stringify({
                    'c_id': c_id,
                })
            };
            $.ajax({
                type: "POST",
                url: "/send",
                data: data,
                dataType: "json",
                success: function (res) {
                    console.log(res);
                    console.log(0)
                    if (res['data'] === '发送成功') {
                        $.message({
                            message: '发送成功',
                            duration: '1000',
                            center: true,
                            type: 'success'
                        });
                        $('#send-btn').attr('disabled', 'disabled')
                    } else {
                        $.message({
                            message: '发送失败',
                            duration: '1000',
                            center: true,
                            type: 'error'
                        });
                    }
                },
                error: function (res) {
                    console.log(res);
                    console.log(1);
                    $.message({
                        message: '服务器连接失败',
                        type: 'warning',
                        duration: 0,
                        showClose: true,
                        center: true,
                        onClose: function () {
                            alert('知道了')
                        }
                    });
                },
            });

    });

    $(function(){
       $('#s_time').val(StartTime())
    });
    $(function(){
       $('#e_time').val(EndTime())
    });


    // input校验
    $(function () {
        // 失去焦点
        $("#modal_c_diameter").blur(check_c_diameter)               // 直径
        $("#modal_c_crown_value").blur(check_c_crown)               // 凸度值
        $("#modal_c_roughness").blur(check_c_roughness)             // 粗糙度
        $("#modal_c_side_bearing").blur(check_c_side_bearing)       // 操作侧轴承号
        $("#modal_c_drive_bearing").blur(check_c_drive_bearing)     // 驱动侧轴承号
        $("#modal_c_pairing_roll").blur(check_c_pairing_roll)       // 配对辊号
        $("#modal_c_top_diameter").blur(check_c_top_diameter)       // 锥形顶端直径
        $("#modal_c_low_diameter").blur(check_c_low_diameter)       // 锥形底端直径
        $("#modal_c_frame_id").blur(check_c_frame_id)               // 机床号
        $("#modal_c_roll_type").blur(check_c_roll_type)             // 轧辊类型
        $("#modal_c_roll_position").blur(check_c_roll_position)     // 轧辊位置
        $("#modal_c_roll_material").blur(check_c_roll_material)     // 轧辊材质
        $("#modal_c_crown_symbol").blur(check_c_crown_symbol)     // 凸度正负标记


    })
    // 直径校验
    function check_c_diameter() {
        // 1.获取凸度值
        var c_crown = $("#modal_c_diameter").val();
        // 2.定义校验正则
        // var reg_username = /^[0-9]{4}$/;
        var reg_c_crown = /^[0-9]{3,4}.[0-9]{3}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 凸度值名合法
            $("#modal_c_diameter").css("border", "");
        } else {
            // 凸度值非法，加一个红色边框
            $("#modal_c_diameter").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 凸度值校验
    function check_c_crown() {
        // 1.获取凸度值
        var c_crown = $("#modal_c_crown_value").val();
        // 2.定义校验正则
        // var reg_username = /^[0-9]{4}$/;
        var reg_c_crown = /^\d{4}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 凸度值名合法
            $("#modal_c_crown_value").css("border", "");
        } else {
            // 凸度值非法，加一个红色边框
            $("#modal_c_crown_value").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 粗糙度校验
    function check_c_roughness() {
        // 1.获取粗糙度
        var c_crown = $("#modal_c_roughness").val();
        // 2.定义校验正则
        var reg_c_crown = /^\d{3}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 粗糙度名合法
            $("#modal_c_roughness").css("border", "");
        } else {
            // 粗糙度非法，加一个红色边框
            $("#modal_c_roughness").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 操作侧轴承号校验
    function check_c_side_bearing() {
        // 1.获取操作侧轴承箱号
        var c_crown = $("#modal_c_side_bearing").val();
        // 2.定义校验正则
        var reg_c_crown = /^[A-Za-z0-9\\-]{8}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 操作侧轴承箱号名合法
            $("#modal_c_side_bearing").css("border", "");
        } else {
            // 操作侧轴承箱号非法，加一个红色边框
            $("#modal_c_side_bearing").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 驱动侧轴承号校验
    function check_c_drive_bearing() {
        // 1.获取驱动侧轴承箱号
        var c_crown = $("#modal_c_drive_bearing").val();
        // 2.定义校验正则
        var reg_c_crown = /^[A-Za-z0-9\\-]{8}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 驱动侧轴承箱号名合法
            $("#modal_c_drive_bearing").css("border", "");
        } else {
            // 驱动侧轴承箱号非法，加一个红色边框
            $("#modal_c_drive_bearing").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 配对辊号校验
    function check_c_pairing_roll() {
        // 1.获取配对辊号
        var c_crown = $("#modal_c_pairing_roll").val();
        // 2.定义校验正则
        var reg_c_crown = /^[A-Za-z0-9\\-]{10}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 配对辊号名合法
            $("#modal_c_pairing_roll").css("border", "");
        } else {
            // 配对辊号非法，加一个红色边框
            $("#modal_c_pairing_roll").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 锥形顶端直径校验
    function check_c_top_diameter() {
        // 1.获取配对辊号
        var c_crown = $("#modal_c_top_diameter").val();
        // 2.定义校验正则
        var reg_c_crown = /^\d{7}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 配对辊号名合法
            $("#modal_c_top_diameter").css("border", "");
        } else {
            // 配对辊号非法，加一个红色边框
            $("#modal_c_top_diameter").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 锥形底端直径校验
    function check_c_low_diameter() {
        // 1.获取配对辊号
        var c_crown = $("#modal_c_low_diameter").val();
        // 2.定义校验正则
        var reg_c_crown = /^\d{7}$/
        // 3.判断是否满足校验要求，并给出提示信息
        var flag = reg_c_crown.test(c_crown);
        if (flag) {
            // 配对辊号名合法
            $("#modal_c_low_diameter").css("border", "");
        } else {
            // 配对辊号非法，加一个红色边框
            $("#modal_c_low_diameter").css("border", "1px solid red");
        }
        // 4.返回是否通过校验
        return flag;
    }

    // 机架号校验
    function check_c_frame_id() {
        // 1.获取配对辊号
        var c_crown = $("#modal_c_frame_id").val();
        // 2.定义校验正则
        var reg_c_crown = "选择机架号"
        // 3.判断是否满足校验要求，并给出提示信息
        var flag
        flag = c_crown != null;

        if (flag){
            $("#modal_c_frame_id_label").css("color","black");

        }
        else {
            $("#modal_c_frame_id_label").css("color","red");
        }

        return flag
    }

    // 轧辊类型校验
    function check_c_roll_type() {
        // 1.获取轧辊类型
        var c_crown = $("#modal_c_roll_type").val();
        // 2.定义校验正则
        var reg_c_crown = "选择轧辊类型"
        // 3.判断是否满足校验要求，并给出提示信息
        var flag
        flag = c_crown != null;

        if (flag){
            $("#modal_c_roll_type_label").css("color","black");

        }
        else {
            $("#modal_c_roll_type_label").css("color","red");
        }

        return flag
    }

    // 轧辊位置校验
    function check_c_roll_position() {
        // 1.获取轧辊位置
        var c_crown = $("#modal_c_roll_position").val();
        // 2.定义校验正则
        var reg_c_crown = "选择轧辊位置"
        // 3.判断是否满足校验要求，并给出提示信息
        var flag
        flag = c_crown != null;

        if (flag){
            $("#modal_c_roll_position_label").css("color","black");

        }
        else {
            $("#modal_c_roll_position_label").css("color","red");
        }

        return flag
    }

    // 轧辊材质校验
    function check_c_roll_material() {
        // 1.获取轧辊材质
        var c_crown = $("#modal_c_roll_material").val();
        // 2.定义校验正则
        var reg_c_crown = "选择轧辊材质"
        // 3.判断是否满足校验要求，并给出提示信息
        var flag
        flag = c_crown != null;

        if (flag){
            $("#modal_c_roll_material_label").css("color","black");

        }
        else {
            $("#modal_c_roll_material_label").css("color","red");
        }

        return flag
    }

    // 凸度正负标记校验
    function check_c_crown_symbol() {
        // 1.获取轧辊材质
        var c_crown = $("#modal_c_crown_symbol").val();
        // 2.定义校验正则
        var reg_c_crown = "选择凸度正负标记"
        // 3.判断是否满足校验要求，并给出提示信息
        var flag
        flag = c_crown != null;

        if (flag){
            $("#modal_c_crown_symbol_label").css("color","black");

        }
        else {
            $("#modal_c_crown_symbol_label").css("color","red");
        }

        return flag
    }

    // 更新操作侧轴承箱号下拉框
    function update_c_side_bearing() {
        $.ajax({
            type:"GET",
            url:"/update_c_side_bearing",
            async:true,
            success:function (data) {
                var c_side_bearing_list = data;
                var rSelect = "<option>——请选择角色——</option>";
                for(var i = 0; i < c_side_bearing_list.length; i++){
                    rSelect += ("<option value = '"+c_side_bearing_list[i].nane+"'>"+c_side_bearing_list[i].name+"</option>");
                }
                $("#modal_c_side_bearing").empty();
                $("#modal_c_side_bearing").append(rSelect);
            }

        })
    }