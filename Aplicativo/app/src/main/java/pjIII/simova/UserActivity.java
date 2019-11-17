package pjIII.simova;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;


public class UserActivity extends AppCompatActivity {

    private TextView atual;
    private TextView textView;
    private TextView evento1;
    private TextView data1;
    private TextView evento2;
    private TextView data2;
    private TextView evento3;
    private TextView data3;
    private TextView evento4;
    private TextView data4;
    private String baseUrl;
    private String um = "Vaga livre e autenticada";
    private String dois = "Vaga livre, porém não autenticada";
    private String tres = "Vaga ocupada e autenticada";
    private String quatro = "Vaga ocupada, porém não autenticada";
    private Button pVaga;
    private Button anterior;
    private ImageButton conf;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user);

        baseUrl = "http://".concat(MainActivity.ip);
        baseUrl = baseUrl.concat(":5000/vaga/" +User.getVaga(2)+"/eventos");

        atual = (TextView) findViewById(R.id.t0);
        textView = (TextView) findViewById(R.id.textView);
        textView.setText(textView.getText()+ User.getVaga(0));
        if(User.getVaga(1) == "1"){
            atual.setText(um);
        }
        else if (User.getVaga(1) == "2"){
            atual.setText(dois);
        }
        else if (User.getVaga(1) == "3"){
            atual.setText(tres);
        }else
            atual.setText(quatro);

        try {
            ApiAuthenticationClient apiAuthenticationClient =
                    new ApiAuthenticationClient(
                            baseUrl
                            , ""
                            , ""
                            ,"GET"
                    );

            AsyncTask<Void, Void, String> ex = new NetworkOperation(apiAuthenticationClient);
            ex.execute();
        } catch (Exception ex) {
        }
        pVaga = (Button) findViewById(R.id.bt01);
        pVaga.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                if(User.vagas.size() > 3){
                    goToUserActivity2();
                }else{
                    Toast.makeText(getApplicationContext(), "O usuário "+User.getNome()+ " não possui mais vagas a serem monitoradas", Toast.LENGTH_LONG).show();
                }
            }

        });
        anterior = (Button) findViewById(R.id.bt00);
        anterior.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                goToUserActivityMain();
            }

        });
        conf = (ImageButton) findViewById(R.id.IB);
        conf.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                goToSettingsActivity();
            }

        });
    }

    private void goToSettingsActivity() {
        Intent intent = new Intent(this, SettingsActivity.class);
        startActivity(intent);
    }

    private void goToUserActivityMain() {
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }

    private void goToUserActivity2() {
        Intent intent = new Intent(this, UserActivity2.class);
        startActivity(intent);
    }

    public void setEventos(){
        evento1 = (TextView) findViewById(R.id.t1);
        data1 = (TextView) findViewById(R.id.t11);
        if(User.eventos.size() >= 2 ){
            evento1.setText(User.getEventos(1));
            data1.setText(User.getEventos(0));
        }else{
            evento1.setText(null);
            data1.setText(null);
        }

        evento2 = (TextView) findViewById(R.id.t2);
        data2 = (TextView) findViewById(R.id.t21);
        if(User.eventos.size() >= 4 ){
            evento2.setText(User.getEventos(3));
            data2.setText(User.getEventos(2));
        }else {
            evento2.setText(null);
            data2.setText(null);
        }

        evento3 = (TextView) findViewById(R.id.t3);
        data3 = (TextView) findViewById(R.id.t31);
        if(User.eventos.size() >= 6 ){
            evento3.setText(User.getEventos(5));
            data3.setText(User.getEventos(4));
        }else {
            evento3.setText(null);
            data3.setText(null);
        }

        evento4 = (TextView) findViewById(R.id.t4);
        data4 = (TextView) findViewById(R.id.t41);
        if(User.eventos.size() >= 8 ){
            evento4.setText(User.getEventos(7));
            data4.setText(User.getEventos(6));
        }else{
            evento4.setText(null);
            data4.setText(null);
        }
    }

    public class NetworkOperation extends AsyncTask<Void, Void, String> {

        private ApiAuthenticationClient apiAuthenticationClient;
        private String isValidCredentials;

        /**
         * Overload the constructor to pass objects to this class.
         */
        public NetworkOperation(ApiAuthenticationClient apiAuthenticationClient) {
            this.apiAuthenticationClient = apiAuthenticationClient;
        }

        @Override
        protected String doInBackground(Void... params) {
            try {
                isValidCredentials = apiAuthenticationClient.ex();
            } catch (Exception e) {
                e.printStackTrace();
            }

            return null;
        }

        @Override
        protected void onPostExecute(String result){
            super.onPostExecute(result);
            if (isValidCredentials == "true"){
                setEventos();
                //Toast.makeText(getApplicationContext(), "Eventos atualizados" , Toast.LENGTH_SHORT).show();
            }else {// Login Failure
                Toast.makeText(getApplicationContext(), "Erro", Toast.LENGTH_LONG).show();
            }
        }
    }
}
