using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TireMC : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        hubTransform = GetComponent<Transform>();
        wheelRigidBody = GetComponent<Rigidbody>();
        //wheelRigidBody.AddRelativeTorque(Vector3.up*-100);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        hubNormalVec = -hubTransform.right;
        rdot = wheelRigidBody.velocity.y;
        


        newRot = Vector3.down;



        if (Physics.Raycast(hubTransform.position, Vector3.forward, out RaycastHit hitinfo, 20f)) {
            r = hitinfo.distance;
            if (r< r0)
            {
                Vector3 normalForce = new Vector3((float)(k * (r - r0) + c * rdot), 0f, 0f);
                wheelRigidBody.AddForce(wheelRigidBody.velocity * -2f, ForceMode.VelocityChange);
            }

        }
        else
        {
            Vector3 normalForce = new Vector3(0f, 0f, 0f);
            wheelRigidBody.AddRelativeForce(normalForce);
        }

        if (Physics.Raycast(hubTransform.position, newRot, out RaycastHit hitinfof, 5f))
        {
            r = hitinfof.distance;
            if (r < r0)
            {
                r = hitinfof.distance;
                Vector3 normalForce2 = -newRot * (float)(k * (r - r0) + c * rdot);
                wheelRigidBody.AddForce(normalForce2);
                wheelRigidBody.AddForce(Vector3.forward * 10);
                wheelRigidBody.AddTorque((wheelRigidBody.velocity.magnitude / r0) * Vector3.right, ForceMode.VelocityChange);

            }
        }

        else
        {
            Vector3 normalForce2 = new Vector3(0f, 0f, 0f);
            wheelRigidBody.AddForce(normalForce2);

        }

        Debug.DrawRay(hubTransform.position, hubNormalVec, Color.red, 10f);
        Debug.Log(hitinfo.distance);
        Debug.DrawRay(hubTransform.position, newRot, Color.blue, 5f);
        Debug.Log(hitinfof.distance);        
        Debug.DrawRay(hubTransform.position, Vector3.forward, Color.green, 5f);
        Debug.Log(hitinfof.distance);

    }
    
    [Tooltip("Unloaded Radius of Tire")]
    public float r0 = .5f;
    [Tooltip("Spring Constant of Tire N/m")]
    public double k = 10;
    [Tooltip("Damping Coefficient of Tire N-s/m")]
    public double c = -.1;
    private double r;
    private double rdot;
    private Vector3 hubNormalVec;
    public Vector3 newRot;
    private Transform hubTransform;
    private Rigidbody wheelRigidBody;

}
