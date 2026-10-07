package cl.jpique.app;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    // Tamaño de letra máximo que se toma del teléfono: más grande desarma las columnas de la app
    private static final float LETRA_MAXIMA = 1.15f;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        float escala = getResources().getConfiguration().fontScale;
        getBridge().getWebView().getSettings().setTextZoom(Math.round(Math.min(escala, LETRA_MAXIMA) * 100));
    }
}
