
//buttonで送信されたか、クリックで送信されたか判断するフラグ
var button=0;

//初期化
$(function () {
    $("#cv").click(reqAstar);

});

//ボタンで送信した場合
function setBtnFlag(){
    button=1;
    $("#cv").click();
}

//位置を送信してパスとパス単語を得る
function reqAstar(e){
    //送信データ準備
    $('#path')[0].innerHTML="";
    //canvasのwidth,height
    var width=$('#cv').outerWidth(true);
    var height=$('#cv').outerHeight(true);
    var tbl=$('#params')[0];
    //単語
    var start=$('#starttxt')[0].value;
    var goal=$('#goaltxt')[0].value;
    var reqLength=$('#spinner')[0].value;

    tbl.rows[0].cells[1].innerHTML=e.offsetX;
    tbl.rows[0].cells[2].innerHTML=e.offsetY;

    //送るデータ
    var data={'x':e.offsetX,
             'y':e.offsetY,
             'sw':start,
             'gw':goal,
             'reqLen':reqLength,
             'isButton':button,

    };
    data=JSON.stringify(data);
    
    var canvas = document.getElementById('cv');

    
    //送信
    $.ajax({
        url: '/aster',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data:JSON.stringify(data),
        timeout: 10000,
    //送信成功
    }).success(function (result) {
        console.log('success');
        //結果を表示
        var res=JSON.stringify(result);
        res=JSON.parse(res);
        var lenC=res["coordinate"].length;
        var lenW=res["pathW"].length;
        //property領域に表示
        tbl.rows[1].cells[1].innerHTML=res["coordinate"][lenC-1][0];
        tbl.rows[1].cells[2].innerHTML=res["coordinate"][lenC-1][1];

        //canvasに描画する
        var canvas = document.getElementById('cv');
        if (canvas.getContext) {
            var context = canvas.getContext('2d');
            context.fillStyle = 'rgb(255,0,0)';
            context.clearRect(0,0,width,height);
            //ラインを描画する
            for(i=0;i<lenC-1;i++){
                context.fillRect(res["coordinate"][i][0],res["coordinate"][i][1],2,2);
            }
            //startとgoal
            context.fillStyle = 'rgb(255,200,100)';
            context.fillRect(res["coordinate"][0][0],res["coordinate"][0][1],6,6);
            context.fillStyle = 'rgb(0,255,0)';
            context.fillRect(res["coordinate"][lenC-1][0],res["coordinate"][lenC-1][1],6,6);
            
            
        }

        $('#path')[0].innerHTML=res["pathW"];
        $('#starttxt')[0].value=res["pathW"][0];
        $('#goaltxt')[0].value=res["pathW"][lenW-1];

    //失敗
    }).fail(function (data, textStatus, errorThrown) {
        console.log('fail');
        alert(errorThrown);
    }).then(function () {
    });
    button=0;
}



