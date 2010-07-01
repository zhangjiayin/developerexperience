package org.opensource.freepic.bean;

import java.util.Date;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.IdentityType;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Blob;
/**
 * 
 * @author	DualR
 * @mail	dualrs@googlemail.com
 * @site	http://www.mimaiji.com
 */
@PersistenceCapable(identityType = IdentityType.APPLICATION)
public class Photo {
	/* id */
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Long id;

	/* title */
	@Persistent
	private String title;

	/* description */
	@Persistent
	private String description;

	/* upload date */
	@Persistent
	private Date date;
	
	@Persistent
	private Blob photo;
	
	public Photo(String title, String description, Date date) {
		this.title = title;
		this.description = description;
		this.date = date;
	}
	public Photo(String title, String description, Date date, Blob photo) {
		this.title = title;
		this.description = description;
		this.date = date;
		this.photo = photo;
	}
	public Photo(Long id, String title, String description, Date date) {
		this.id = id;
		this.title = title;
		this.description = description;
		this.date = date;
	}
	public Blob getPhoto() {
		return photo;
	}

	public void setPhoto(Blob photo) {
		this.photo = photo;
	}

	public Photo(Blob photo){
		this.photo = photo;
	}

	public Photo(String title, Date date, Blob img) {
		this.title = title;
		this.date = date;
		this.photo =img;
	}
	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}
	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Date getDate() {
		return date;
	}

	public void setDate(Date date) {
		this.date = date;
	}

}