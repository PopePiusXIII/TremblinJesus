using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tire : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Time.fixedDeltaTime = .001f;
        hubTransform = GetComponent<Transform>();
        wheelRigidBody = GetComponent<Rigidbody>();
        wheelRotateBody = hubTransform.Find("Visual").gameObject.GetComponent<Rigidbody>();
        wheelRotateTransform = hubTransform.Find("Visual").gameObject.GetComponent<Transform>();
        wheelRotateBody.maxAngularVelocity = 10000f;
        wheelRotateBody.angularVelocity = new Vector3(0f, 0f, -2f);
        wheelRotateTransform.localPosition = new Vector3(0f,0f,0f);
        wheelRigidBody.velocity = hubTransform.right * 1;
        arrowT = hubTransform.Find("FX").gameObject.GetComponent<Transform>();
        arrowx = new Arrow(arrowT, wheelRigidBody, 0f, 1f, 0f, 1f);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        arrowx.Change();
        hubNormalVec = -hubTransform.forward;   //this is dumb notation need to figure out how to fix
        rdot = hubTransform.InverseTransformDirection(wheelRigidBody.velocity).z;
        if (Physics.Raycast(hubTransform.position, hubNormalVec, out RaycastHit hitinfo, 5 * r0))
        {
            r = hitinfo.distance;
            if (r < r0)
            {
                normalForce = (k * (r - r0) + c * rdot);
                longitudinalForce = LongitudinalForce(wheelRigidBody, hitinfo);
            }

            else
            {
                r = r0;
                normalForce = 0;
                longitudinalForce = LongitudinalForce(wheelRigidBody, hitinfo);
                longitudinalForce = 0;
            }
        }

        wheelRigidBody.AddRelativeForce(new Vector3(longitudinalForce, 0, normalForce));
        wheelRotateBody.AddRelativeTorque(new Vector3(0f, -longitudinalForce * r + motorTorque, 0f)); ;
        wheelRotateTransform.localPosition = new Vector3(0f, 0f, 0f);

        Debug.Log("r:" + r + "rdot:  " + rdot+  " fz:" + normalForce);
        Debug.DrawRay(hubTransform.position, r * hubNormalVec, Color.red, .1f, false);
    }

    float FxModel(float slipRatio, float normalForce)
    {
        return fxSlope * normalForce * slipRatio;
    }

    float LongitudinalForce(Rigidbody wheel, RaycastHit hitinfo)
    {
        float omegaTire = hubTransform.InverseTransformDirection(wheelRotateBody.angularVelocity).y;
        float contactPatchVx = omegaTire * r;
        float hubVx = hubTransform.InverseTransformDirection(wheel.velocity).x;

        Debug.Log("hubvx: " + hubVx + " contact patch vx: " + contactPatchVx + "slip ratio: " + slipRatio);
        Debug.Log("fx:" + longitudinalForce);

        if (Mathf.Abs(hubVx) < .001) slipRatio = contactPatchVx;
        else
        {
            slipRatio = contactPatchVx / hubVx - 1;
            slipRatio = Mathf.Sign(slipRatio) * Mathf.Min(Mathf.Abs(slipRatio), .1f);
        }
        //return FxModel(slipRatio, normalForce);
        return 0;
    }


    [Tooltip("Unloaded Radius of Tire")]
    public float r0 = .5f;
    [Tooltip("Spring Constant of Tire N/m")]
    public float k = -10f;
    [Tooltip("Damping Coefficient of Tire N-s/m")]
    public float c = -1f;
    private float r;
    private float rdot;
    private float normalForce;
    public float longitudinalForce;
    public float slipRatio;
    public float motorTorque;
    public float fxSlope;
    private Vector3 hubNormalVec;
    public Vector3 newRot;
    private Transform hubTransform;
    private Rigidbody wheelRigidBody;
    private Rigidbody wheelRotateBody;
    private Transform wheelRotateTransform;
    private Transform arrowT;
    private Arrow arrowx;


}
