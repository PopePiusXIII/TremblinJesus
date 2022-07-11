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

        Transform arrowT = hubTransform.Find("FZ").gameObject.GetComponent<Transform>();
        arrowz = new Arrow(arrowT, 1f, 100f);
        arrowT = hubTransform.Find("FX").gameObject.GetComponent<Transform>();
        arrowx = new Arrow(arrowT, 1f, 100f);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        hubNormalVec = -hubTransform.forward;   //this is dumb notation need to figure out how to fix
        rdot = hubTransform.InverseTransformDirection(wheelRigidBody.velocity).z;
        if (Physics.Raycast(hubTransform.position, hubNormalVec, out RaycastHit hitinfo, 5 * r0))
        {
            r = hitinfo.distance;
            if (r < r0)
            {
                Fz = (k * (r - r0) + c * rdot);
                slipRatio = slipRatioModel(wheelRigidBody, hitinfo);
                Fx = FxModel();
            }

            else
            {
                r = r0;
                Fz = 0;
                slipRatio = 0;
                Fx = 0;
                Fx = 0;
            }
        }

        wheelRigidBody.AddRelativeForce(new Vector3(Fx, 0, Fz));
        wheelRotateBody.AddRelativeTorque(new Vector3(0f, -Fx * r + motorTorque, 0f)); ;
        wheelRotateTransform.localPosition = new Vector3(0f, 0f, 0f);

        Debug.Log("r:" + r + "rdot:  " + rdot+  " fz:" + Fz);
        Debug.DrawRay(hubTransform.position, r * hubNormalVec, Color.red, .1f, false);

        arrowz.Change(Fz);
        arrowx.Change(Fx);
    }

    float FxModel()
    {
        return fxSlope * Fz * slipRatio;
    }

    float slipRatioModel(Rigidbody wheel, RaycastHit hitinfo)
    {
        float omegaTire = hubTransform.InverseTransformDirection(wheelRotateBody.angularVelocity).y;
        float contactPatchVx = omegaTire * r;
        float hubVx = hubTransform.InverseTransformDirection(wheel.velocity).x;

        Debug.Log("hubvx: " + hubVx + " contact patch vx: " + contactPatchVx + "slip ratio: " + slipRatio);
        Debug.Log("fx:" + Fx);

        if (Mathf.Abs(hubVx) < .001) slipRatio = contactPatchVx;
        else
        {
            slipRatio = contactPatchVx / hubVx - 1;
            slipRatio = Mathf.Sign(slipRatio) * Mathf.Min(Mathf.Abs(slipRatio), .1f);
        }
        return slipRatio;
    }


    [Tooltip("Unloaded Radius of Tire")]
    public float r0 = .5f;
    [Tooltip("Spring Constant of Tire N/m")]
    public float k = -10f;
    [Tooltip("Damping Coefficient of Tire N-s/m")]
    public float c = -1f;
    private float r;
    private float rdot;
    public float Fz;
    public float Fx;
    public float slipRatio;
    public float motorTorque;
    public float fxSlope;
    private Vector3 hubNormalVec;
    public Vector3 newRot;
    private Transform hubTransform;
    private Rigidbody wheelRigidBody;
    private Rigidbody wheelRotateBody;
    private Transform wheelRotateTransform;
    private Arrow arrowx;
    private Arrow arrowz;


}
