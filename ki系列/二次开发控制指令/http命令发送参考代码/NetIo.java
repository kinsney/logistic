//By jaosn 2013-6-28
package hs.avr_io_panel;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.OutputStreamWriter; 
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.URL;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;
import android.text.Editable;
import android.util.Log;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;


public class NetIo 
{

    private Socket client;
    private String ip;
    private int port;
    private int timeout_ms = 10000;
    public static final int PORTA = 0;
	public static final int PORTB = 1;
	public static final int PORTC = 2;
	public static final int PORTD = 3;
	
    
	
	
    public NetIo(String ip, int port)
    {
        this.ip = ip;
        this.port = port;
    }
   
    public NetIo(String ip, int port, int timeout_ms)
    {
        this.ip = ip;
        this.port = port;
        this.timeout_ms = timeout_ms;
    }

    
    public boolean connect()
    {
        boolean connected = false;
        try {

            client = new Socket();
            client.connect(new InetSocketAddress(ip, port), timeout_ms);
            PrintStream output = new PrintStream( client.getOutputStream() );
			BufferedReader input = new BufferedReader( new InputStreamReader( client.getInputStream() ) );
             connected = true;

        } catch (UnknownHostException ex) {
            Logger.getLogger(AvrNetIo.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(AvrNetIo.class.getName()).log(Level.SEVERE, null, ex);
        }
        return connected;
    }

    /**
     * Disconnect Methode
     */
    public void disconnect()
    {
        try {
            client.close();
        } catch (IOException ex) {
            Logger.getLogger(AvrNetIo.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

   
    public boolean isConnected()
    {
        return client.isConnected();
    }


    
    private String sendData(String msg)
    {
        String line = "";
        if(isConnected())
        {
            try {
                PrintWriter out = new PrintWriter(client.getOutputStream());
                BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                out.println(msg + "\r\n");
                out.flush();
                line = in.readLine();                
                line = line.replaceAll("\0", "").replaceAll("\r\n", "").trim();
                
                in.close();
                out.close();
            } catch (IOException ex) {
            	Log.e("Kommunikations Klasse:","Fehler: " + ex.getMessage() );
                //Logger.getLogger(AvrNetIo.class.getName()).log(Level.SEVERE, null, ex);
            } catch (Exception ex) {
            	Log.e("Kommunikations Klasse:","Fehler: " + ex.getMessage());
            }
        }
        return line;
    }

    
    public int getADC(int port)
    {
        if(port < 1 || port > 4)
        {
            return -1;
        }
        String result = sendData("GETADC "+port);
        int value = 0;
        
        if (result.length() > 0)
        	try{
        		value = Integer.parseInt(result);
        	}
        catch (Exception ex){
        	Log.e("Kommunikations Klasse:","Integer Parse Error");
        	return -1;
        }
        return value;
    }

    public boolean setOutPort(int port, boolean level)
    {
        if(port < 1 || port > 8)
        {
            return false;
        }
        char levelchar = level ? '1' : '0';
        return sendData("SETPORT "+port+"."+levelchar).equals("ACK");
    }
    //
    public void setOutput(String ipp,int port, int bitNum, boolean value)
	{
		int mask = (1 << bitNum);
		int set = 0;
		if (value)
			set = (1 << bitNum);

		setValue(ipp,"port", port, set, mask);
	}
    private void setValue(String type, int port, int value)
	{   
    	String urlSt="http://"+ "192.168.1.88";
		String msg =
				"/ecmd?"+
			"io%20set%20" +
			type + "%20" +
			port +
			"%20" +
			Integer.toHexString(value);
		urlSt+=msg;
		try {
			URL url = new URL(urlSt);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
	        conn.connect();
	        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(),"utf-8"));
	        String lines;
	        while ((lines = reader.readLine()) != null){
	        	//lines = new String(lines.getBytes(), "utf-8");
	            System.out.println(lines);
	        }
	        System.out.println("=============================");
	        System.out.println("Contents of http request");
	        System.out.println("=============================");
	       // this.device.request(urlSt);
	        reader.close();
	        conn.disconnect();
	        //  conn.setDoOutput(true);
	      //  conn.getOutputStream().flush();
	      //  conn.getOutputStream().close();
	     //   conn.getInputStream().close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
    
	public void setDDR(int port, int value)
	{
		setValue("ddr", port, value);
	}

	public void setDDR(String ipp,int port, int pin, boolean value)
	{
		int mask = (1 << pin);
		int set = 0;
		if (value)
			set = (1 << pin);

		setValue(ipp,"ddr", port, set, mask);
	}
	private void setValue(String iphost,String type, int port, int value, int mask)
	{   
	
		
	String urlSt="http://"+iphost;
		String msg =
				"/ecmd?"+
			"io%20set%20"+
			type +
			"%20" +
			port +
			"%20" +
			Integer.toHexString(value) +
			"%20" +
			Integer.toHexString(mask);
		urlSt+=msg;
		try {
			URL url = new URL(urlSt);
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
	        conn.connect();
	        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(),"utf-8"));
	        String lines;
	        while ((lines = reader.readLine()) != null){
	        	lines = new String(lines.getBytes(), "utf-8");
	            System.out.println(lines);
	        }
	        System.out.println("=============================");
	        System.out.println("Contents of http1 request");
	        System.out.println("=============================");
	        reader.close();
	        conn.disconnect();
	        
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
    private EditText findViewById(int edittext01) {
		// TODO Auto-generated method stub
		return null;
	}
	
    public int getOutPort(int port)
    {

        if(port <  1 || port > 8)
        {
            return -1;
        }

        String answer = sendData("GETSTATUS");

        if(answer.length() > 1 && answer.length() < 10 && answer.startsWith("S"))
        {
            return Integer.parseInt(""+answer.charAt(port));
        }
        return -1;
    }

    
    public String getStatus()
    {
        return sendData("GETSTATUS");
    }

   
    public String getIP()
    {
        return sendData("GETIP");
    }

   
    public boolean setIP(String ip)
    {
        return sendData("SETIP "+ip).equals("ACK");
    }

    
    public String getMask()
    {
        return sendData("GETMASK");
    }

    
    public boolean setMask(String mask)
    {
        return sendData("SETMASK "+mask).equals("ACK");
    }


    
    public String getGW()
    {
        return sendData("GETGW");
    }

    public boolean setGW(String gw)
    {
        return sendData("SETGW "+gw).equals("ACK");
    }

    public boolean initLCD()
    {
        return sendData("INITLCD").equals("ACK");
    }

    public boolean writeLCD(int line, String txt)
    {
        boolean answer = false;
        if(line == 1 || line == 2)
        {
            answer = sendData("WRITELCD "+line+"."+txt).equals("ACK");
        }
        return answer;
    }

    
    public void clearLCD(int line)
    {
        if(line == 1 || line == 2)
        {
            sendData("CLEARLCD "+line);
        }
        else
        {
            sendData("CLEARLCD");
        }
    }

    
    public String getVersion()
    {
        return sendData("VERSION");
    }




}


