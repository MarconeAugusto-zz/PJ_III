package pjIII.simova;


import android.os.Parcel;
import android.os.Parcelable;

public class Usuario implements Parcelable {

    private String uuid;
    private String username;
    private String token;
    private boolean online;

    public Usuario() {
    }

    public Usuario(String uuid, String username) {
        this.uuid = uuid;
        this.username = username;
    }

    protected Usuario(Parcel in) {
        uuid = in.readString();
        username = in.readString();
        token = in.readString();
        online = in.readInt() == 1;
    }

    public static final Creator<Usuario> CREATOR = new Creator<Usuario>() {
        @Override
        public Usuario createFromParcel(Parcel in) {
            return new Usuario(in);
        }

        @Override
        public Usuario[] newArray(int size) {
            return new Usuario[size];
        }
    };

    public String getUuid() {
        return uuid;
    }

    public String getUsername() {
        return username;
    }

    public String getToken() {
        return token;
    }

    public boolean isOnline() {
        return online;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(uuid);
        dest.writeString(username);
        dest.writeString(token);
        dest.writeInt(online ? 1 : 0);
    }

}

