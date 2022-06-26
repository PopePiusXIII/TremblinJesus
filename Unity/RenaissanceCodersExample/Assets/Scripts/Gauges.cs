using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Gauges : MonoBehaviour
{
    public Rigidbody target;
    private const float MAX_SPEED_ANGLE = -127;
    private const float ZERO_SPEED_ANGLE = 144;
    private Transform needleTransform;
    private float speedMax;
    private float speed;

    private void Awake()
    {
        needleTransform = transform.Find("needle");
        speed = 0f;
        speedMax = 160f;
    }

    private void Update()
    {
        speed = target.velocity.magnitude * 3.6f;
        if (speed > speedMax) speed = speedMax;

        needleTransform.eulerAngles = new Vector3(0, 0, GetSpeedRotation());
    }

    private float GetSpeedRotation()
    {
        float totalAngleSize = ZERO_SPEED_ANGLE - MAX_SPEED_ANGLE;
        float speedNormalized = speed / speedMax;

        return ZERO_SPEED_ANGLE - speedNormalized * totalAngleSize;
    }
}
