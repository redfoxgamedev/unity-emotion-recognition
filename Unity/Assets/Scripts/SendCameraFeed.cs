using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.Networking;

public class SendCameraFeed : MonoBehaviour
{
    [SerializeField]
    private string apiUrl = "http://127.0.0.1:5000/api/predict";

    [SerializeField]
    private Webcam webcam = default;

    [SerializeField]
    private bool sendEveryFrame = default;

    public event Action<string> ResponseReceived;
    private Coroutine emotionRequest;

    private void Update()
    {
        if (sendEveryFrame && emotionRequest == null)
        {
            SendWebCameraImage();
        }
        else
        {
            if (Input.GetKeyDown(KeyCode.P))
            {
                SendWebCameraImage();
            }
        }
    }

    private void SendWebCameraImage()
    {
        Color32[] imageDataColor32 = webcam.WebcamTexture.GetPixels32();

        //TODO: ad-hoc solution, the only quick way to know whether web cam was initialized
        bool webCameraInitialized = imageDataColor32.Length != 256;
        if (webCameraInitialized == false)
        {
            return;
        }

        PostMessageJson postMessageJson = new PostMessageJson()
        {
            imageData = Color32ArrayToByteArray(imageDataColor32)
        };

        string jsonBody = JsonUtility.ToJson(postMessageJson);
        emotionRequest = StartCoroutine(PostRequest(apiUrl, jsonBody));
    }

    private IEnumerator PostRequest(string url, string jsonBody)
    {
        UnityWebRequest request = new UnityWebRequest(url, "POST");
        byte[] rawBody = new System.Text.UTF8Encoding().GetBytes(jsonBody);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(rawBody);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();
        PostMessageResponse response = JsonUtility.FromJson<PostMessageResponse>(request.downloadHandler.text);

        if (request.isHttpError || request.isNetworkError)
        {
            Debug.LogWarning("Request returned web error");
            emotionRequest = null;
            yield break;
        }

        Debug.Log("Emotion: " + response.emotion);
        ResponseReceived?.Invoke(response.emotion);

        emotionRequest = null;
    }

    private class PostMessageJson
    {
        public byte[] imageData;
    }

    private class PostMessageResponse
    {
        public string emotion;
    }

    private static byte[] Color32ArrayToByteArray(Color32[] colors)
    {
        if (colors == null || colors.Length == 0)
            return null;

        int lengthOfColor32 = Marshal.SizeOf(typeof(Color32));
        int length = lengthOfColor32 * colors.Length;
        byte[] bytes = new byte[length];

        GCHandle handle = default(GCHandle);
        try
        {
            handle = GCHandle.Alloc(colors, GCHandleType.Pinned);
            IntPtr ptr = handle.AddrOfPinnedObject();
            Marshal.Copy(ptr, bytes, 0, length);
        }
        finally
        {
            if (handle != default(GCHandle))
                handle.Free();
        }

        return bytes;
    }
}
