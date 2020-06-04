using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeTextOnEmotion : MonoBehaviour
{
    [SerializeField]
    private TMPro.TMP_Text text = default;

    [SerializeField]
    private SendCameraFeed cameraFeed = default;

    private void OnEnable()
    {
        cameraFeed.ResponseReceived += OnEmotionReceived;
    }

    private void OnDisable()
    {
        cameraFeed.ResponseReceived -= OnEmotionReceived;
    }

    private void OnEmotionReceived(string emotion)
    {
        text.text = emotion;
    }
}
