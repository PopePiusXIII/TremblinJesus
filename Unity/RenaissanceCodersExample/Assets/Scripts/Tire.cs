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
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        hubNormalVec = -hubTransform.right;
        rdot = wheelRigidBody.velocity.y;
        


        newRot = Quaternion.AngleAxis(-90, -hubTransform.up) * hubNormalVec;



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

        if (Physics.Raycast(hubTransform.position, newRot, out RaycastHit hitinfof, 5f))
        {
            r = hitinfof.distance;
            if (r < r0)
            {
                r = hitinfof.distance;
                Vector3 normalForce2 = -newRot * (float)(k * (r - r0) + c * rdot);
                wheelRigidBody.AddRelativeForce(normalForce2);
            }
        }

        else
        {
            Vector3 normalForce = new Vector3(0f, 0f, 0f);
            wheelRigidBody.AddRelativeForce(normalForce);

        }

        Debug.DrawRay(hubTransform.position, hubNormalVec, Color.red, .1f);
        Debug.Log(hitinfo.distance);
        Debug.DrawRay(hubTransform.position, newRot*.5f, Color.blue, .1f);
        Debug.Log(hitinfof.distance);

    }
    
    [Tooltip("Unloaded Radius of Tire")]
    public double r0 = .5;
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
