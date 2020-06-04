using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayOnUserEmotion : MonoBehaviour
{
    [SerializeField]
    private ParticleSystem particleSystem = default;

    [SerializeField]
    private SendCameraFeed cameraFeed = default;

    [SerializeField]
    private string matchEmotion = default;

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
        if (emotion.ToLower().Equals(matchEmotion.ToLower()))
        {
            particleSystem.Play();
        }
        else
        {
            particleSystem.Stop(false, ParticleSystemStopBehavior.StopEmittingAndClear);
        }
    }
}
