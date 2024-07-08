using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class PythonTest : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI pythonRcvdText = null;
    [SerializeField] TextMeshProUGUI sendToPythonText = null;

    string tempStr = "OCR Text:";
    int numToSendToPython = 0;
    UdpSocket udpSocket;

    public void QuitApp()
    {
        print("Quitting");
        Application.Quit();
    }

    public void UpdatePythonRcvdText(string str)
    {
        tempStr = str;
    }

    public void SendToPython()
    {

        udpSocket.SendData("Sent From Unity: " + numToSendToPython.ToString());
        numToSendToPython++;
        sendToPythonText.text = "Start OCR: " + (numToSendToPython-1).ToString();
    }

    private void Start()
    {
        udpSocket = FindObjectOfType<UdpSocket>();
        sendToPythonText.text = "Start OCR";
    }

    void Update()
    {
        pythonRcvdText.text = tempStr;
    }
}
