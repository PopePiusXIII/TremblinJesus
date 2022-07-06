using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tire : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        hubTransform = GetComponent<Transform>();
        wheelRigidBody = GetComponent<Rigidbody>();
        wheelRotateBody = hubTransform.Find("Visual").gameObject.GetComponent<Rigidbody>();
        wheelRotateTransform = hubTransform.Find("Visual").gameObject.GetComponent<Transform>();
        wheelRotateBody.angularVelocity = -wheelRotateTransform.up * wheelRigidBody.velocity.z / r0;
        wheelRotateTransform.localPosition = new Vector3(0f,0f,0f);
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
                Vector3 normalForce = new Vector3((float)(k * (r - r0) + c * rdot), 0f, 0f);
                wheelRigidBody.AddRelativeForce(normalForce);
            }

        }
        else
        {
            Vector3 normalForce = new Vector3(0f, 0f, 0f);
            wheelRigidBody.AddRelativeForce(normalForce);
        }

        if (Physics.Raycast(hubTransform.position, hubTransform.forward, out RaycastHit hitinfof, 5f))
        {
            r = hitinfof.distance;
            if (r < r0)
            {
                r = hitinfof.distance;
                Vector3 normalForce2 = -hubTransform.forward * (float)(k * (r - r0) + c * rdot);
                wheelRigidBody.AddRelativeForce(normalForce2);
            }
        }

        else
        {
            Vector3 normalForce = new Vector3(0f, 0f, 0f);
            wheelRigidBody.AddRelativeForce(normalForce);

        }

        wheelRotateTransform.localPosition = new Vector3(0f, 0f, 0f);
        wheelRotateBody.angularVelocity = -wheelRotateTransform.up * wheelRigidBody.velocity.z / r0;
        Debug.DrawRay(hubTransform.position, hubNormalVec, Color.red, .1f);
        Debug.Log(hitinfo.distance);
        Debug.DrawRay(hubTransform.position, hubTransform.forward*.5f, Color.blue, 3f);
        Debug.Log(hitinfof.distance);

    }
    
    [Tooltip("Unloaded Radius of Tire")]
    public float r0 = 0.5f;
    [Tooltip("Spring Constant of Tire N/m")]
    public double k = 10;
    [Tooltip("Damping Coefficient of Tire N-s/m")]
    public double c = -.1;
    private double r;
    private double rdot;
    private Vector3 hubNormalVec;
    private Transform hubTransform;
    private Rigidbody wheelRigidBody;
    private Rigidbody wheelRotateBody;
    private Transform wheelRotateTransform;

}
