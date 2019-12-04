package pjIII.simova;

import android.util.Log;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;


/**
 * Agosto, 02 2019
 *
 * @author suporte@moonjava.com.br (Tiago Aguiar).
 */
public class FCMService extends FirebaseMessagingService{

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        Log.i("Teste",remoteMessage.getMessageId());
    }

}
