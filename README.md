# CCU SSO維持登入

> [!WARNING]
> 被資訊處約談不要找我
>
> 資訊處也不要找我約談

## 1. Description

從單一入口登入後的[選單](https://portal.ccu.edu.tw/sso_index.php)可以看到以下javascript

```javascript
// from https://portal.ccu.edu.tw/sso_index.php
var session_refresh_time = 595; // session更新間隔
var session_maxrefresh_time = 7200; // session持續更新的最大時限
var interval_id = '';
var last_activity_time = '';
$(document).ready(function() {
	var date_obj = new Date();
        last_activity_time = Math.floor(date_obj.getTime() / 1000); // milliseconds
        interval_id = setInterval(refresh_timer, session_refresh_time * 1000);  //就是這行 讓他5950毫秒執行一次 他是非同步執行的
	.
	.
	.
}
.
.
.
function refresh_timer() {
	var d = new Date();
        var now_time = Math.floor(d.getTime() / 1000);
        var total_time = now_time - last_activity_time;
        if (now_time - last_activity_time <= session_maxrefresh_time) {
		$.post('ajax/refresh_time_ajax.php');
	} else {
		clearInterval(interval_id);
        }
}
.
.
.
```

* 原理: 每595秒發送一個POST請求到https://portal.ccu.edu.tw/ajax/refresh_time_ajax.php告訴伺服器我還活著

  我推測他後端的設定是10分鐘沒有任何動作的話session會失效被登出

  每次POST請求之後會獲得f5avraaaaaaaaaaaaaaaa_session跟一個TS01C三小的cookie

  這兩個不用理他

  再根據下面這段javascript

  ```javascript
  // from https://portal.ccu.edu.tw/sso_index.php
  function onSignOn(event) {
      $.ajax({
          url: 'ajax/refresh_time_ajax.php',
          cache: false,
          type: 'POST',
          data: {
              type: 'is_alive'
          },
          success: function(response) {
              if (response.search('s_expire') != -1) {
                  location.replace('logout_check.php');
              }
          }
      });

      var linkId = $(this).attr('name');
      var service = '';
      var para = '';
      var jsonStr = '{"i0037":".\/test_eCourse2.php","i0100":"https:\/\/ssas.ccu.edu.tw\/mdb2\/sso.2.php","i0003":"\/test_0003_Lib.php","i0028":"https:\/\/cross-school.ccu.edu.tw\/","i0044":"\/test_eDoc.php","i0060":"\/test_Lib_iActivity_Apply.php","i0064":"\/test_0064_StuOff.php","i0029":"\/test_0029_Approve.php","i0001":"http:\/\/coursemap.ccu.edu.tw\/include\/SSO\/getssoCcuRight.php","i0021":"\/test_Duty.php","i0021p":"https:\/\/miswww1.ccu.edu.tw\/dutysyspg\/getssoCcuRight.php","i0002":"\/test_Kiki.php","i0002g":"\/prod_Kiki.php","i0022":"\/test_Personal.php","i0023":"\/test_Accounting.php","i0057":"\/test_Lib_Explorer.php","i0058":"\/test_Lib_EResource.php","i0059":"\/test_Lib_Space_Reserves.php","i0042":"\/test_payment.php","i0004":"\/test_Academic.php","i0024":"\/test_Profession.php","i0055":"\/test_Loan.php","i0005":"\/test_AcademicGra.php","i0025":"\/test_AMS.php","i0006":"\/test_ePortfolio.php","i0026":"\/test_salary.php","i0007":"\/test_0007_GradeQuery.php","i0007g":"\/test_0007g_GradeQuery.php","i0030":"\/test_Consume.php","i0008":"\/test_0008_Software.php","i0031":"\/test_Project.php","i0009":"\/test_GradDormApply.php","i0043":"\/test_EHSC.php","i0053":"\/test_DeductApply.php","i0010":"\/test_DormApply.php","i0011":"\/test_DormRepair.php","i0012":"\/test_Exemption.php","i0013":"\/test_Support.php","i0014":"\/test_Parttime.php","i0015":"\/test_0015_VoteTrans.php","i0054":"\/test_Qualify.php","i0067":"\/test_0067_Leave.php","i0016":"https:\/\/ecard.ccu.edu.tw\/getPermission","i0017":"http:\/\/infotest.ccu.edu.tw\/elearn_func\/getssoCcuRight.php","i0018":"https:\/\/onlinestudy.ccu.edu.tw\/getssoCcuRight.php","i0019":"\/test_Booking.php","i0020":"https:\/\/affairs.ccu.edu.tw\/getssoCcuRight.php","i0027":"https:\/\/www026190.ccu.edu.tw\/hostel\/getssoCcuRight.php","i0032":"\/test_NUCloud.php","i0033":"https:\/\/card.ccu.edu.tw\/","i0034":"http:\/\/ipsc.ccu.edu.tw\/login","i0035":"https:\/\/startupland.ccu.edu.tw\/","i0040":"\/test_CCUComment.php","i0000":"https:\/\/ecourse.ccu.edu.tw\/php\/getssoCcuRight.php","i0065":"\/test_0065_DormWifiApply.php","i0068":"\/test_0068_MicroCredit.php","i0063":"\/test_0063_CarApply.php","i0061":"\/test_HV.php","i0056":"\/test_Student_Off.php","i0066":"\/test_0066_Publication.php","i0045":"\/test_RTS.php","i0069":"\/test_0069_AIM-HI.php","i0070":"\/test_0070_Insurance.php","i10000":"https:\/\/ssas.ccu.edu.tw\/mdb2\/redirect\/redirect_kernel.php","i10001":"https:\/\/ssas.ccu.edu.tw\/mdb2\/redirect\/redirect_kernel.php","i10002":"https:\/\/ssas.ccu.edu.tw\/mdb2\/redirect\/redirect_core.php"}';
      var targetUrlsJson = JSON.parse(jsonStr);
      var user = '才不給你看我的學號勒';
      var iLink = 'i' + linkId;
      service = targetUrlsJson[iLink];
      signOn(service, linkId, para);
  }

  function signOn(service, linkId, para) { // 
      if (service != '') {
          var targetUrl = 'https://portal.ccu.edu.tw/ssoService.php?service=' + service + '&linkId=' + linkId + '&para=' + para;
          window.open(targetUrl, linkId);
      } else {
          alert('Unknown service!');
      }
  }
  ```

  用GET方式去'https://portal.ccu.edu.tw/ssoService.php?service=' + service + '&linkId=' + linkId + '&para=' + para
  可以在單一入口選單打開原始碼看linkid

  ```html
  <li class="panel-icon">
  	<a href="javascript:void(0);" name="0060">
  		<div class="my-icons my-icons-i0060"></div>
  		<p>活動報名<br>系統</p>
  	</a>
  </li>
  ```

  e.g. [eCourse2](https://portal.ccu.edu.tw/ssoService.php?service=./test_eCourse2.php&linkId=0037&para=): https://portal.ccu.edu.tw/ssoService.php?service=./test_eCourse2.php&linkId=0037&para=
  實測需要帶ccuSSO, JSESSIONID, TGC這三個cookie

  再進行一些後續轉跳就可以登入[eCourse2](https://portal.ccu.edu.tw/ssoService.php?service=./test_eCourse2.php&linkId=0037&para=)，這就是我們平常按下按鈕背後的原理

  同理，可以拿來登入[智慧化活動暨報名系統](https://events.lib.ccu.edu.tw/)拿到sessionid再拿到csrfmiddlewaretoken來搶服務學習講座

  jsonStr已經格式化好放在map.json裡了，注意跳脫字元

## 2. Requirement

| 套件    | 版本 |
| ------- | ---- |
| re      |      |
| request |      |
| time    |      |

## 3. Usage

##### JSESSIONID, TGC 獲取

在[單一入口SSO登入的頁面(打帳號密碼還有Google recaptcha的那個地方  你要理解成校慶煙火那頁面也行)](cas.ccu.edu.tw)打開DevTools，選擇Network分頁，上方勾選保留紀錄

![image](https://github.com/chimingwang69/ccuSSO_keep_login/blob/main/img/1.png)

接著打帳號密碼，按好Google recpatcha並登入，從login的response header可以看到Set-Cookie 複製JSESSIONID和TGC的值       後面的Path都不管他

![image](https://github.com/chimingwang69/ccuSSO_keep_login/blob/main/img/2.png)

##### ccuSSO獲取

上圖的https://portal.ccu.edu.tw/login_check_cas.php?ticket=點進去可以看到Set-Cookie ccuSSO=xxx 複製起來，不要包含 ;

###### 最後填好下面 請注意useragent必須和當前登入的瀏覽器一模一樣，不然無法登入

```python
# 全名 用來檢查是否登入成功 
name = ''
# cookie
ccuSSO = 'xxxxx'
TGC = 'xxxxx'  #這串他媽有夠長的 686個字元
JSESSIONID= 'xxx'

# header
useragent = ''
```

接著可以看到成功登入，拿到[eCourse2](https://portal.ccu.edu.tw/ssoService.php?service=./test_eCourse2.php&linkId=0037&para=)的MoodleSession和[智慧化活動暨報名系統](https://events.lib.ccu.edu.tw/)的sessionid了

![image](https://github.com/chimingwang69/ccuSSO_keep_login/blob/main/img/3.png)

## 4. Note

* 未來如果選課系統改強制用sso登入，可以參考這篇自己寫一個新的，不然2Captcha要錢欸，如果說加選頁面也有recaptcha，那另當別論。
* 測試時發現伺服端疑似有限制單一帳號的session數量，要用ecourse2時盡量用手機moodle，如果不得已要使用到單一入口，可以順手更新三個cookies
