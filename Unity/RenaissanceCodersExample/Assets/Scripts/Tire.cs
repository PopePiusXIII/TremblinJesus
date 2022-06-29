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
        Physics.Raycast(hubTransform.position, hubNormalVec, out RaycastHit hitinfo, 20f);
        if (hitinfo.distance < r0) {
            r = hitinfo.distance;
            Vector3 normalForce = new Vector3((float)(k * (r - r0) + c * rdot), 0f, 0f);
            wheelRigidBody.AddRelativeForce(normalForce);
        }
        else {
            r = 0;
            Vector3 normalForce = new Vector3(0f, 0f, 0f);
            wheelRigidBody.AddRelativeForce(normalForce);
        }
        Debug.DrawRay(hubTransform.position, hubNormalVec, Color.red, 100f);
        Debug.Log(hitinfo.distance);

    }
  
    private double r0 = .5;
    public double k = 10;
    public double c = -.1;
    public double r;
    public double rdot;
    public Vector3 hubNormalVec;
    private Transform hubTransform;
    private Rigidbody wheelRigidBody;

}
