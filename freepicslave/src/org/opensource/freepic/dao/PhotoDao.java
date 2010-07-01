package org.opensource.freepic.dao;

import java.util.ArrayList;
import java.util.List;

import javax.jdo.PersistenceManager;
import javax.jdo.Query;

import org.opensource.freepic.bean.Photo;


/**
 * 
 * @author	DualR
 * @mail	dualrs@googlemail.com
 * @site	http://www.mimaiji.com
 */
public class PhotoDao {
	private static PhotoDao _instance = null;

	public static PhotoDao getInstance() {
		if (_instance == null) {
			_instance = new PhotoDao();
		}
		return _instance;
	}

	//save photo
	public String insertPhoto(Photo photo) {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		try {
			pm.makePersistent(photo);
		} finally {
			pm.close();
		}
		return photo.getId().toString();
	}

	//get photo by id
	@SuppressWarnings("unchecked")
	public Photo getById(Long id) {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Query query = pm.newQuery(Photo.class);
		query.setFilter("id == idParam");
		query.declareParameters("Long idParam");
		List<Photo> photo = null;
		try {
			photo = (List<Photo>) query.execute(id);
			if (photo.isEmpty()){
				return null;
			}else{
				return photo.get(0);
			}
			
		} finally {
			query.closeAll();
		}
	}
	//get photo by id
	public Photo getByPid(Long id){
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Photo photo = pm.getObjectById(Photo.class,id);
		return photo;
	}

	//get photo list
	@SuppressWarnings("unchecked")
	public List<Object[]> getAllByPage(int indexStart, int indexEnd) {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Query query = pm.newQuery(Photo.class);
		query.setRange(indexStart, indexEnd);
		query.setOrdering("date desc");
		query.setResult("id, title, date, description");
		List<Object[]> photo = new ArrayList();
		try {
			photo = (List<Object[]>) query.execute();
			return photo;
		} finally {
			query.closeAll();
		}
	}

	// get counts
	public int getCount() {
		String sql = "SELECT count(id) FROM org.dualr.lite.album.bean.Photo";
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Query query = pm.newQuery(sql);
		int i;
		try {
			i = (Integer) query.execute();
			return i;
		} finally {
			query.closeAll();
		}
	}
	
	// delete photo by id
	@SuppressWarnings("unchecked")
	public boolean deleteById(Long id) {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Query query = pm.newQuery(Photo.class);
		query.setFilter("id == idParam");
		query.declareParameters("Long idParam");
		List<Photo> photos = (List<Photo>) pm.newQuery(query).execute(id);
		try {
			for (Photo photo : photos) {
				pm.deletePersistent(photo);
			}
		} finally {
			pm.close();
		}
		return true;
	}

	/**
	 * @param photo
	 */
	//update photo property
	public void update(Photo photo) {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		try {
			Photo p = pm.getObjectById(Photo.class, photo.getId());
			p.setTitle(photo.getTitle());
			p.setDate(photo.getDate());
			p.setDescription(photo.getDescription());
			
		} finally {
			pm.close();
		}
		
	}


}