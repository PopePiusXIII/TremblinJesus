using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EngineSound : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        double speed = carRigidBody.transform.InverseTransformDirection(carRigidBody.velocity)[2];
        double pitch = speed / 100 * pitchRateFudge + min_pitch;
        if (pitch > max_pitch)
            pitch = max_pitch;
        else if (pitch < min_pitch)
            pitch = min_pitch;
        Debug.Log(speed);

        engingeAudioSource.pitch = (float) pitch;


    }
    public double min_pitch = .5;
    public double max_pitch = 1.1;
    public AudioSource engingeAudioSource;
    public Rigidbody carRigidBody;
    public float pitchRateFudge = 2;
}
