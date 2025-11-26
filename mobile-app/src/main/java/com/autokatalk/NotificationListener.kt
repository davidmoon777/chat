package com.autokatalk


import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.content.Intent
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch


class NotificationListener : NotificationListenerService() {
private val TAG = "NotifListener"


override fun onNotificationPosted(sbn: StatusBarNotification) {
val pkg = sbn.packageName ?: return
// 카카오톡 패키지 이름 확인 (기기별로 다를 수 있음)
if (!pkg.contains("kakao")) return


val extras = sbn.notification.extras
val title = extras.getString("android.title") ?: ""
val text = extras.getCharSequence("android.text")?.toString() ?: ""


// 단순화: 채팅방은 title, 메시지는 text
Log.d(TAG, "Kakao notif - $title: $text")


// 서버에 메시지 보냄
CoroutineScope(Dispatchers.IO).launch {
try {
NetworkClient.postIncoming(chatId = title, sender = title, message = text)
} catch (e: Exception) {
Log.e(TAG, "Network error: ${e.localizedMessage}")
}
}
}
}
