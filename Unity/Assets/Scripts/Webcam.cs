using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Webcam : MonoBehaviour
{
    [SerializeField]
    private Renderer renderer = default;
    public Renderer Renderer => renderer;

    private WebCamTexture webcamTexture;
    public WebCamTexture WebcamTexture => webcamTexture;

    // Start is called before the first frame update
    void Awake()
    {
        Application.RequestUserAuthorization(UserAuthorization.WebCam);
        webcamTexture = new WebCamTexture(640, 480, 60);
        //Debug.Log("Real width and height: " + webcamTexture.width + " and " + webcamTexture.height);
        renderer.material.mainTexture = webcamTexture;
        webcamTexture.Play();
    }

    
}
