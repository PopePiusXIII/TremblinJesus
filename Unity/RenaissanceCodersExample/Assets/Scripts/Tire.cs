using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tire : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Time.fixedDeltaTime = .01f;
        hubTransform = GetComponent<Transform>();
        wheelRigidBody = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        hubNormalVec = -hubTransform.right;
        rdot = wheelRigidBody.velocity.y;
        

        if (Physics.Raycast(hubTransform.position, hubNormalVec, out RaycastHit hitinfo, 20f)) {
            r = hitinfo.distance;
            if (r< r0)
            {
                normalForce = (k * (r - r0) + c * rdot);
                longitdudinalForce = LongitudinalForce(wheelRigidBody, hitinfo);
            }

        }
        else
        {
            r = r0;
            normalForce = 0;
            longitdudinalForce = 0;
        }
        wheelRigidBody.AddRelativeForce(new Vector3(normalForce, 0f, longitdudinalForce));

        Debug.DrawRay(hubTransform.position, hubNormalVec, Color.red, .1f);
        Debug.Log(hitinfo.distance);
    }

    float FxModel(float slipRatio, float normalForce)
    {
        float slipStiffness = 31.4f;
        float angularDrag = 1f;
        return normalForce * Mathf.Sin(slipStiffness * slipRatio) - angularDrag * slipRatio;
    }

    float LongitudinalForce(Rigidbody wheel, RaycastHit hitinfo)
    {
        r = hitinfo.distance;
        float contactPatchVx = omega_wheel * r;
        slipRatio = (contactPatchVx - wheel.velocity[1]) / Mathf.Abs(wheel.velocity[1]);
        return FxModel(slipRatio, normalForce);
    }

    void HubTorqueBalance()
    {
        float motorTorque = 100;
        omega_wheel += (longitdudinalForce - motorTorque) / wheelRigidBody.inertiaTensor[1] * Time.fixedDeltaTime;
    }


    [Tooltip("Unloaded Radius of Tire")]
    public float r0 = .5f;
    [Tooltip("Spring Constant of Tire N/m")]
    public float k = 10f;
    [Tooltip("Damping Coefficient of Tire N-s/m")]
    public float c = -.1f;
    private float r;
    private float rdot;
    private float normalForce;
    private float longitdudinalForce;
    private float slipRatio;
    private float omega_wheel = 0;
    private Vector3 hubNormalVec;
    public Vector3 newRot;
    private Transform hubTransform;
    private Rigidbody wheelRigidBody;

}
