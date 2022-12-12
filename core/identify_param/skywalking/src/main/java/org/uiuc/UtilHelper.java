package org.uiuc;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class UtilHelper {

  public static void copy(InputStream in, OutputStream out) throws IOException {
    while (true) {
      int c = in.read();
      if (c == -1)
        break;
      out.write((char) c);
    }
  }
}
