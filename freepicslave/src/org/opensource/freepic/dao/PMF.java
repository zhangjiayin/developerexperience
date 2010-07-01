package org.opensource.freepic.dao;

import javax.jdo.JDOHelper;
import javax.jdo.PersistenceManagerFactory;
/**
 * 
 * @author	DualR
 * @mail	dualrs@googlemail.com
 * @site	http://www.mimaiji.com
 */
public class PMF {
    private static final PersistenceManagerFactory pmfInstance =
        JDOHelper.getPersistenceManagerFactory("transactions-optional");

    private PMF() {}

    public static PersistenceManagerFactory get() {
        return pmfInstance;
    }
}